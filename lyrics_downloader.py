from PyQt4.QtCore import QObject, SIGNAL
from lyrics_cacher import LyricsCacher
from cachebuilder_progress_bar import Ui_cachebuilderProgressDialog

#In the future I plan to make this self enumerating but for now we need to list all providers:
from lyricsProviders import lyricswiki, songlyrics
provider_classes = [lyricswiki.LyricsProvider, songlyrics.LyricsProvider]

class threadedLyricsDownloader(QObject):
    def __init__(self, song, artist):
        self.song = song
        self.artist = artist
        self.lyricsCache = LyricsCacher()
        self.providers = [p() for p in provider_classes]
        super(threadedLyricsDownloader, self).__init__()

    def doWork(self):
        lyrics = self.getUpdatedLyrics()
        self.emit(SIGNAL("lyricsUpdate"), lyrics)
        self.emit(SIGNAL("workFinished()"))

    def getUpdatedLyrics(self, forced=False):
        #Check our cache, and download if missing
        for p in self.providers:
            lyrics = p.getLyrics(self.song, self.artist)
            if lyrics is not None:
                self.last_return = [self.song, self.artist]
                self.lyricsCache.saveLyrics(self.song, self.artist, lyrics)
                return lyrics
        providerlist = ", ".join([p.LYRICS_PROVIDER_NAME for p in self.providers])
        return "Couldn't find lyrics for '%s' by %s. <br><br>Tried following lyrics providers: %s" % (self.song, self.artist, providerlist)