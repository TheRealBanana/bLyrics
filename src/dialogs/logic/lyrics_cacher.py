import os
import os.path
import re
from base64 import urlsafe_b64encode#, urlsafe_b64decode

#This folder is located two folder below the main src folder
#src/dialogs/logic
#Get the folder path two folders up, minus the filename = -3
#Using os.getcwd() instead of the below works 90% of the time (problems arise with windows shortcuts without start-in dir set).
#The below works 100% of the time unless someone messes with the source tree.
BASEPATH = os.sep.join(re.split(re.escape(os.sep), os.path.realpath(__file__))[:-3])
CACHEWRITEFOLDER = os.path.join(BASEPATH, ".lyricscache")

BASE64TEMPLATE = "%(ARTIST)s___%(SONG)s"
FILEEXTENSION = ".blyrics.txt"
HTMLBREAKREGEX = re.compile("<br( /)?>", flags=re.I|re.M)

class LyricsCacher(object):
    def __init__(self):
        self.checkLyricsDir()

    @staticmethod
    def getCachefilePath(song, artist):
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
        files = self.getLyricsFileList()
        if self.getCachefilePath(song, artist) in files:
            return True
        else:
            return False

    def getLyrics(self, song, artist):
        filepath = os.path.join(CACHEWRITEFOLDER, self.getCachefilePath(song, artist))
        try:
            with open(filepath, 'r') as lyricsfile:
                return lyricsfile.read().replace("\n", "<br>")
        except Exception as e:
            print "Well that shouldn't have happened..."
            print e

    def saveLyrics(self, song, artist, lyrics):
        savepath = os.path.join(CACHEWRITEFOLDER, self.getCachefilePath(song, artist))
        #Most of the returned lyrics are html with <br>'s instead of proper line-breaks
        if len(lyrics.splitlines()) > 1:
            #Looks like we have newlines already, remove any br's and hope it looks fine
            lyrics = HTMLBREAKREGEX.sub("", lyrics)
        else:
            lyrics = HTMLBREAKREGEX.sub(os.linesep, lyrics)
        try:
            lyrics = lyrics.encode("utf8")
        except: pass
        #Make sure our cache directory is there and ready to be written
        if self.checkLyricsDir():
            try:
                with open(savepath, mode='w') as lyricsfile:
                    lyricsfile.write(lyrics)
            except:
                print "There was an error saving the lyrics for '%s' by %s to file" % (song, artist)

    def getCacheSize(self):
        return len(self.getLyricsFileList())

    def clearLyricsCache(self):
        print "Clearing Lyrics Cache..."
        filelist = self.getLyricsFileList()
        for f in filelist:
            os.remove(os.path.join(CACHEWRITEFOLDER, f))
        return len(filelist)

    #Search all cached lyrics for songs that contain the supplied strings
    #The similarityFactor is a float value between 0 and 1 that describes how
    #close a match the searched string must be.
    #1.0 is exact match, 0.0 matches any string. 0.65 is a nice starting value.
    def searchLyrics(self, strings=[], similarityFactor=1.0):
        pass