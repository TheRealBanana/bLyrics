import os
import os.path
import re
import sys
import sqlite3
from base64 import urlsafe_b64encode, urlsafe_b64decode
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import SIGNAL, QObject

#This folder is located two folder below the main src folder
#src/dialogs/logic
#Get the folder path two folders up, minus the filename = -3
#Using os.getcwd() instead of the below works 90% of the time (problems arise with windows shortcuts without start-in dir set).
#The below works 100% of the time unless someone messes with the source tree.
#
#If we are running from the pyinstaller .exe we need to modify things
if getattr(sys, 'frozen', False):
    BASEPATH = os.sep.join(re.split(re.escape(os.sep), sys.executable)[:-1])
else:
    BASEPATH = os.sep.join(re.split(re.escape(os.sep), os.path.realpath(__file__))[:-3])
# running live

CACHEWRITEFOLDER = os.path.join(BASEPATH, ".lyricscache")
DATABASE_NAME = "blyrics.db"
DATABASE_PATH = os.path.join(CACHEWRITEFOLDER, DATABASE_NAME)

BASE64SEP = "___"
BASE64TEMPLATE = "%(ARTIST)s"+BASE64SEP+"%(SONG)s"
FILEEXTENSION = ".blyrics.txt"
HTMLBREAKREGEX = re.compile("<br( /)?>", flags=re.I|re.M)

#Trying out something new, hoping this will make the code cleaner
class getDbCursor(object):
    def __init__(self, dbpath, contype='r'):
        self.dbpath = dbpath
        self.contype = contype
        self.dbhandle = None
        self.dbcursor = None
    def __enter__(self):
        self.dbhandle = sqlite3.connect(self.dbpath)
        self.dbcursor = self.dbhandle.cursor()
        return self.dbcursor
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.contype == 'w':
            self.dbhandle.commit()
        self.dbhandle.close()

class LyricsCacher(object):
    def __init__(self):
        if self.checkForLyricsDb() is False: self.disableCache()
        self.filelist = self.getLyricsFileList()
        self.cachedLyrics = None
        self.loadedIntoMem = False
        self.cancel = False

    #Been a while since ive done any db stuff so its all a bit rusty. Im trying to only have the db open while an
    #operation is happening. That means lots of duplicate code but meh.
    @staticmethod
    def checkForLyricsDb():
        #Check if we have a folder and if not create it
        if os.access(CACHEWRITEFOLDER, os.F_OK) is False:
            try:
                os.makedirs(CACHEWRITEFOLDER)
            except:
                return False
        #Now see if we have a database file and if not create a new one
        if os.access(DATABASE_PATH, os.W_OK):
            with getDbCursor(DATABASE_PATH) as dbcursor:
                try:
                    table_list = dbcursor.execute("SELECT name FROM sqlite_master where type='table' ORDER BY name").fetchone()
                except sqlite3.DatabaseError:
                    return False
            #Make sure this is our database
            if table_list is None or table_list[0] != "blyrics_data":
                return False
            else:
                return True

        else:
            # No database file exists so we are going to create it and try and
            # populate it with old-style cache file if they exist.

            with getDbCursor(DATABASE_PATH, 'w') as dbcursor:
                #Lyrics table
                dbcursor.execute("CREATE TABLE blyrics_data ("
                                 "song TEXT,"
                                 "artist TEXT,"
                                 "failedtries INTEGER,"
                                 "lyrics TEXT,"
                                 "PRIMARY KEY (song, artist)"
                                 ")")
            print "Created new lyrics database file."
            return True

    def convertOldCache(self, progressbar):
        cachefilelist = self.getLyricsFileList()
        #Set up our progressbar
        progressbar.progressBar.setMaximum(len(cachefilelist))
        progressbar.progressLabel.setText("Converting old lyrics cache into new format...")
        QObject.connect(progressbar.cancelButton, SIGNAL("clicked()"), self.cancelConvert)
        progressbar.progressBar.setValue(0)
        print "Converting cached lyrics to new database format..."
        songlistsize = len(cachefilelist)
        addnum = 0
        self.cancel = False
        for idx, filename in enumerate(cachefilelist):
            if self.cancel:
                break

            filepath = os.path.join(".", CACHEWRITEFOLDER, filename)
            #Decode the filename to get artist/song name
            b64part = filename[:-len(FILEEXTENSION)]
            decoded = urlsafe_b64decode(b64part)
            artist, song = re.split(BASE64SEP, decoded)

            #nice place to update progressbar
            progressbar.progressLabel.setText("Converting old cache into new format...\n(%s/%s) Found cached lyrics for: %s by %s" % (idx+1, songlistsize, song, artist))
            progressbar.progressBar.setValue(idx+1)
            QApplication.processEvents()

            with open(filepath, 'r') as f:
                lyrics = f.read()
            #Write to db
            if self.saveLyrics(song, artist, lyrics, noupdate=True) is True:
                addnum += 1

        print "Finished converting cache files. Added %s new song lyrics out of %s cache files." % (addnum, len(cachefilelist))
        return addnum, len(cachefilelist)




    @staticmethod
    def getCachefileName(song, artist):
        return "%s%s" % (urlsafe_b64encode(BASE64TEMPLATE % {"SONG": song, "ARTIST": artist}), FILEEXTENSION)

    #Not sure if this is the best way to do this but It works without fiddling with return values/ifs
    @staticmethod
    def noCacheForYou(*_, **__):
        return None

    def disableCache(self):
        #Ok no cache for you!
        print "NO CACHE FOR YOU!"
        self.checkSong = self.noCacheForYou
        self.getLyrics = self.noCacheForYou
        self.searchLyrics = self.noCacheForYou

    @staticmethod
    def getLyricsFileList():
        #Only our cache files
        return [f for f in os.listdir(CACHEWRITEFOLDER) if
                (os.path.isfile(os.path.join(CACHEWRITEFOLDER, f)) is True and
                (re.match("^.*%s$" % re.escape(FILEEXTENSION), f)) is not None)]

    #For now this is exact matching now. Later we may use the b64decode()'d string
    #with SequenceMatcher to check for almost matches. Not sure yet.
    @staticmethod
    def checkSong(song, artist):
        #Cause python2 we have to do some unicode handling
        if not isinstance(song, unicode): song = unicode(song, "utf-8")
        if not isinstance(artist, unicode): artist = unicode(artist, "utf-8")
        with getDbCursor(DATABASE_PATH) as dbcursor:
            data = dbcursor.execute("SELECT COUNT(1) FROM blyrics_data WHERE song=? AND artist=?", (song, artist)).fetchone()
        return bool(data[0])

    @staticmethod
    def searchLyricsCache(song, artist, lyricsstring):
        if not isinstance(song, unicode): song = unicode(song, "utf-8")
        if not isinstance(artist, unicode): artist = unicode(artist, "utf-8")
        if not isinstance(lyricsstring, unicode): lyricsstring = unicode(lyricsstring, "utf-8")

        with getDbCursor(DATABASE_PATH) as dbcursor:
            results = dbcursor.execute("SELECT song, artist FROM blyrics_data WHERE artist LIKE ? AND song LIKE ? AND lyrics LIKE ?", (artist, song, lyricsstring)).fetchall()
        return results

    @staticmethod
    def getLyrics(song, artist):
        if not isinstance(song, unicode): song = unicode(song, "utf-8")
        if not isinstance(artist, unicode): artist = unicode(artist, "utf-8")
        with getDbCursor(DATABASE_PATH) as dbcursor:
            data = dbcursor.execute("SELECT lyrics FROM blyrics_data where song=? AND artist=?", (song, artist)).fetchone()
        return data[0].replace("\n", "<br>")

    def saveLyrics(self, song, artist, lyrics, noupdate=False):
        if not isinstance(song, unicode): song = unicode(song, "utf-8")
        if not isinstance(artist, unicode): artist = unicode(artist, "utf-8")
        if not isinstance(lyrics, unicode): lyrics = unicode(lyrics, "utf-8")

        if len(lyrics.splitlines()) > 1:
            #Looks like we have newlines already, remove any br's and hope it looks fine
            lyrics = HTMLBREAKREGEX.sub("", lyrics)
        else:
            lyrics = HTMLBREAKREGEX.sub(os.linesep, lyrics)

        with getDbCursor(DATABASE_PATH, 'w') as dbcursor:
            #Are we setting new lyrics or updating old ones?
            if self.checkSong(song, artist) is False:
                dbcursor.execute("INSERT INTO blyrics_data VALUES (?,?,?,?)", (song, artist, 0, lyrics))
            elif noupdate is False:
                dbcursor.execute("UPDATE blyrics_data SET lyrics=? WHERE song=? AND artist=?", (lyrics, song, artist))
            else:
                return False
        return True

    @staticmethod
    def getCacheSize():
        with getDbCursor(DATABASE_PATH) as dbcursor:
            data = dbcursor.execute("SELECT COUNT(*) FROM blyrics_data").fetchone()
        return data[0]

    #TODO FIXME
    """
    def clearLyricsCache(self):
        print "Clearing Lyrics Cache..."
        filelist = self.getLyricsFileList()
        for f in filelist: # Dangerous, only remove blyrics.txt files.
            os.remove(os.path.join(CACHEWRITEFOLDER, f))
        return len(filelist)
    """

    def cancelConvert(self):
        self.cancel = True