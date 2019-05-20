import os
import os.path
import re
import sys
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

BASE64SEP = "___"
BASE64TEMPLATE = "%(ARTIST)s"+BASE64SEP+"%(SONG)s"
FILEEXTENSION = ".blyrics.txt"
HTMLBREAKREGEX = re.compile("<br( /)?>", flags=re.I|re.M)

class LyricsCacher(object):
    def __init__(self):
        self.checkLyricsDir()
        self.filelist = self.getLyricsFileList()
        #Structure of cachedLyrics:
        # cachedLyrics[artist_name][song_name]=lyrics
        self.cachedLyrics = None
        self.loadedIntoMem = False
        self.cancel = False

    @staticmethod
    def getCachefileName(song, artist):
        return "%s%s" % (urlsafe_b64encode(BASE64TEMPLATE % {"SONG": song, "ARTIST": artist}), FILEEXTENSION)

    #Now sure if this is the best way to do this but It works without fiddling with return values/ifs
    @staticmethod
    def noCacheForYou(*_, **__):
        return None

    def getLyricsFileList(self):
        #Only our cache files
        if self.checkLyricsDir():
            return [f for f in os.listdir(CACHEWRITEFOLDER) if \
                (os.path.isfile(os.path.join(CACHEWRITEFOLDER, f)) is True and \
                (re.match("^.*%s$" % re.escape(FILEEXTENSION), f)) is not None)]
        else:
            return []

    #Create lyrics directory if necessary (if posible, if not disable cache access)
    def checkLyricsDir(self):
        #Check if we have access to the cache folder
        if os.access(CACHEWRITEFOLDER, os.F_OK) is False:
            try:
                os.makedirs(CACHEWRITEFOLDER)
                return True
            except:
                #Ok no cache for you!
                self.checkSong = self.noCacheForYou
                self.getLyrics = self.noCacheForYou
                self.searchLyrics = self.noCacheForYou
        else:
            return True
        print "There was a problem creating the lyrics cache folder."
        return False

    #For now this is exact matching now. Later we may use the b64decode()'d string
    #with SequenceMatcher to check for almost matches. Not sure yet.
    def checkSong(self, song, artist):
        if self.loadedIntoMem:
          if self.cachedLyrics.has_key(artist) and self.cachedLyrics[artist].has_key(song):
              return True
          else:
              return False
        elif self.getCachefileName(song, artist) in self.filelist:
            return True
        else:
            return False

    def getLyrics(self, song, artist):
        if self.loadedIntoMem:
            if self.cachedLyrics.has_key(artist) and self.cachedLyrics[artist].has_key(song):
                return self.cachedLyrics[artist][song].replace("\n", "<br>")
        #Try to load from disk if we arent loaded into mem or the memory cache missed.
        filepath = os.path.join(CACHEWRITEFOLDER, self.getCachefileName(song, artist))
        try:
            with open(filepath, 'r') as lyricsfile:
                return lyricsfile.read().replace("\n", "<br>")
        except Exception as e:
            print "Well that shouldn't have happened..."
            print e

    def saveLyrics(self, song, artist, lyrics):
        print "saving lyrics for %s by %s: %s" % (song, artist, len(lyrics))
        savepath = os.path.join(CACHEWRITEFOLDER, self.getCachefileName(song, artist))
        #Most of the returned lyrics are html with <br>'s instead of proper line-breaks
        if len(lyrics.splitlines()) > 1:
            #Looks like we have newlines already, remove any br's and hope it looks fine
            lyrics = HTMLBREAKREGEX.sub("", lyrics)
        else:
            lyrics = HTMLBREAKREGEX.sub(os.linesep, lyrics)
        try:
            lyrics = unicode(lyrics).encode("utf8")
        except: pass
        #Make sure our cache directory is there and ready to be written
        if self.checkLyricsDir():
            try:
                with open(savepath, mode='w') as lyricsfile:
                    lyricsfile.write(lyrics)
            except:
                print "There was an error saving the lyrics for '%s' by %s to file" % (song, artist)
        self.filelist.append(self.getCachefileName(song, artist))
        if self.cachedLyrics is not None:
            if not self.cachedLyrics.has_key(artist):
                self.cachedLyrics.artist = {}
            self.cachedLyrics[artist][song] = lyrics

    def getCacheSize(self):
        return len(self.getLyricsFileList())

    def clearLyricsCache(self):
        print "Clearing Lyrics Cache..."
        filelist = self.getLyricsFileList()
        for f in filelist:
            os.remove(os.path.join(CACHEWRITEFOLDER, f))
        return len(filelist)

    def cancelPreload(self):
        self.cancel = True

    #Reading from the hdd is slow, even for an ssd. Might as well trade memory for speed.
    def preloadLyricsCacheIntoMemory(self, progressbar_ui):
        #Delete the old data
        del self.cachedLyrics
        self.cachedLyrics = {}
        self.cancel = False
        self.loadedIntoMem = False
        filelist = self.getLyricsFileList()
        totalsongs = len(filelist)
        progressbar_ui.progressBar.setMaximum(totalsongs)
        progressbar_ui.progressLabel.setText("Loading cache into memory...")
        QObject.connect(progressbar_ui.cancelButton, SIGNAL("clicked()"), self.cancelPreload)
        for idx, filename in enumerate(filelist):
            if self.cancel is True:
                print "Canceled loading cache into memory"
                return

            progressbar_ui.progressBar.setValue(idx)
            QApplication.processEvents()

            b64part = filename[:-len(FILEEXTENSION)]
            decoded = urlsafe_b64decode(b64part)
            artist, song = re.split(BASE64SEP, decoded)

            if not self.cachedLyrics.has_key(artist):
                self.cachedLyrics[artist] = {}
            lyricsfilepath = os.path.join(CACHEWRITEFOLDER, filename)
            with open(lyricsfilepath, 'r') as lyricsfile:
                self.cachedLyrics[artist][song] = unicode(lyricsfile.read()).decode("utf8")

        self.loadedIntoMem = True
        print "Done loading cache into memory"