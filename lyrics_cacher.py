import os
import re
import os.path
from base64 import urlsafe_b64encode#, urlsafe_b64decode

CACHEWRITEFOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), ".lyricscache")
BASE64TEMPLATE = "%s___%s"
FILEEXTENSION = ".blyrics.txt"

class LyricsCacher(object):
    def __init__(self):
        #Check if we have access to the cache folder
        if os.access(CACHEWRITEFOLDER, os.F_OK) is False:
            try:
                os.makedirs(CACHEWRITEFOLDER)
            except:
                #Ok no cache for you!
                self.checkSong = self.noCacheForYou
                self.getLyrics = self.noCacheForYou
                self.searchLyrics = self.noCacheForYou

    #Now sure if this is the best way to do this but It works without fiddling with return values/ifs
    def noCacheForYou(self, *_, **__):
        return None

    def getLyricsFileList(self):
        #Only our cache files
        return [f for f in os.listdir(CACHEWRITEFOLDER) if \
                (os.path.isfile(os.path.join(CACHEWRITEFOLDER, f)) is True and \
                (re.match("^.*%s$" % re.escape(FILEEXTENSION), f)) is not None)]

    #For now this is exact matching now. Later we may use the b64decode()'d string
    #with SequenceMatcher to check for almost matches. Not sure yet.
    def checkSong(self, song, artist):
        files = self.getLyricsFileList()
        if "%s%s" % (urlsafe_b64encode(BASE64TEMPLATE % (song, artist)), FILEEXTENSION) in files:
            return True
        else:
            return False

    def getLyrics(self, song, artist):
        filepath = os.path.join(CACHEWRITEFOLDER, "%s%s" % (urlsafe_b64encode(BASE64TEMPLATE % (song, artist)), FILEEXTENSION))
        try:
            with open(filepath, 'r') as lyricsfile:
                return lyricsfile.read().replace("\n", "<br>")
        except Exception as e:
            print "Well that shouldn't have happened..."
            print e

    def saveLyrics(self, song, artist, lyrics):
        savepath = os.path.join(CACHEWRITEFOLDER, "%s%s" % (urlsafe_b64encode(BASE64TEMPLATE % (song, artist)), FILEEXTENSION))
        with open(savepath, mode='w') as lyricsfile:
            lyricsfile.write(lyrics)

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