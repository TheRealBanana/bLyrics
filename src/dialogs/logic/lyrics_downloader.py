from PyQt4.QtCore import QObject, SIGNAL
from ntpath import basename
import os
import os.path
import re
import sys

#I hate this function. I had such an awesomely simple setup using __import__() but pyinstaller just has to be ornery
#After much tinkering this is the only solution I've found that works under normal python and pyinstaller's bundled python

class lyricsProviders(object):
    def __init__(self):
        self.providerList = self.enumerateProviders() # No custom priorities initially, have to run initProviderList().

    def initProviderList(self, saved_priorities):
        self.providerList = self.enumerateProviders(saved_priorities)

    def enumerateProviders(self, saved_priorities={}):
        provider_classes = []
        if getattr(sys, 'frozen', False):
            providerdir = os.path.join(sys._MEIPASS, "lyricsProviders")
            listdir = "./"
        else:
            providerdir = os.sep.join(re.split(re.escape(os.sep), os.path.realpath(__file__))[:-1])
            listdir = "./lyricsProviders/"
        os.chdir(providerdir)
        sys.path.append(providerdir)
        filelist = [re.match("^(.*)\.py$", x).group(1) for x in os.listdir(listdir) if os.path.isfile(listdir+x) and re.match("^.*\.py$", x) and x != "__init__.py"]
        importlist = __import__("lyricsProviders", fromlist=filelist, level=0)
        for f in filelist:
            if f in dir(importlist):
                l = getattr(importlist, f)
                if hasattr(l, "LyricsProvider"):
                    provider_classes.append(l)
        #Now sort the provider classes by priority from lowest to highest
        #Set a default priority if we dont have one
        for p in provider_classes:
            p.LyricsProvider.ENABLED = True
            if hasattr(p, "LYRICS_PROVIDER_PRIORITY") is False:
                p.LYRICS_PROVIDER_PRIORITY = 10 # Default priority is 10
            #TODO WILL APPLY CUSTOM PRIORITIES HERE
            if saved_priorities.has_key(basename(p.__file__)):
                p.LYRICS_PROVIDER_PRIORITY = saved_priorities[basename(p.__file__)]["priority"]
                p.LyricsProvider.ENABLED = saved_priorities[basename(p.__file__)]["enabled"]

        return sorted(provider_classes, key=lambda provider: provider.LYRICS_PROVIDER_PRIORITY)


class threadedLyricsDownloader(QObject):
    def __init__(self, song, artist, lyricsCacheRef, providerListRef, customProvider=None):
        self.song = song
        self.artist = artist
        self.lyricsCache = lyricsCacheRef
        self.providers = [p.LyricsProvider() for p in providerListRef.providerList]
        self.customProvider = customProvider
        super(threadedLyricsDownloader, self).__init__()

    def doWork(self):
        lyrics, providername = self.getUpdatedLyrics()
        self.emit(SIGNAL("lyricsUpdate"), lyrics, providername)
        self.emit(SIGNAL("workFinished()"))

    def getUpdatedLyrics(self):
        #Are we being asked to retrieve from a specific source only?
        if self.customProvider is not None:
            try:
                lyrics = self.customProvider.getLyrics(self.song, self.artist)
            except Exception as e:
                return ("There was an error retrieving from %s:<br><br>%s" % (self.customProvider.LYRICS_PROVIDER_NAME, e), None)
            if lyrics is not None:
                self.last_return = [self.song, self.artist]
                self.lyricsCache.saveLyrics(self.song, self.artist, lyrics)
                return (lyrics, self.customProvider.LYRICS_PROVIDER_NAME)
            else:
                return ("Couldn't find lyrics for '%s' by %s from %s." % (self.song, self.artist, self.customProvider.LYRICS_PROVIDER_NAME), None)
        else:
            for p in self.providers:
                if p.ENABLED is False:
                    continue
                try:
                    lyrics = p.getLyrics(self.song, self.artist)
                    if lyrics is not None:
                        self.last_return = [self.song, self.artist]
                        self.lyricsCache.saveLyrics(self.song, self.artist, lyrics)
                        return (lyrics, p.LYRICS_PROVIDER_NAME)
                except:
                    continue
            providerlist = ", ".join([p.LYRICS_PROVIDER_NAME for p in self.providers])
            return ("Couldn't find lyrics for '%s' by %s. <br><br>Tried following lyrics providers: %s" % (self.song, self.artist, providerlist), None)