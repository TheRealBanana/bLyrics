from PyQt4.QtCore import QObject, SIGNAL
from lyrics_cacher import LyricsCacher
import os
import os.path
import re
import sys

#I hate this function. I had such an awesomely simple setup using __import__() but pyinstaller just has to be ornery
#After much tinkering this is the only solution I've found that works under normal python and pyinstaller's bundled python
def enumerateProviders():
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
        if hasattr(p, "LYRICS_PROVIDER_PRIORITY") is False:
            p.LYRICS_PROVIDER_PRIORITY = 10 # Default priority is 10
    return sorted(provider_classes, key=lambda provider: provider.LYRICS_PROVIDER_PRIORITY)


class threadedLyricsDownloader(QObject):
    def __init__(self, song, artist):
        self.song = song
        self.artist = artist
        self.lyricsCache = LyricsCacher()
        self.providers = [p.LyricsProvider() for p in enumerateProviders()]
        super(threadedLyricsDownloader, self).__init__()

    def doWork(self):
        lyrics, providername = self.getUpdatedLyrics()
        self.emit(SIGNAL("lyricsUpdate"), lyrics, providername)
        self.emit(SIGNAL("workFinished()"))

    def getUpdatedLyrics(self):
        #Check our cache, and download if missing
        for p in self.providers:
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