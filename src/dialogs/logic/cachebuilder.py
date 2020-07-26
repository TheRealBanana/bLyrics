from PyQt4 import QtCore, QtGui
from PyQt4.Qt import QApplication
from time import sleep


try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class threadedCacheGenerator(QtCore.QObject):
    def __init__(self, songdata, lyricsCacheRef, providerListRef):
        self.songdata = songdata
        self.totalsongs = len(self.songdata["playlist"])
        self.quitting = False
        self.lyricsCacheRef = lyricsCacheRef
        self.providers = [p.LyricsProvider() for p in providerListRef.providerList]
        super(threadedCacheGenerator, self).__init__()

    def getUpdatedLyrics(self, song, artist):
        #Check our cache, and download if missing
        for p in self.providers:
            if self.quitting is True: return None, None
            try:
                lyrics = p.getLyrics(song, artist)
            except:
                continue
            if lyrics is not None:
                try:
                    lyrics = lyrics.encode("utf8")
                except:
                    pass
                self.lyricsCacheRef.saveLyrics(song, artist, lyrics)
                return (lyrics, p.LYRICS_PROVIDER_NAME)
        providerlist = ", ".join([p.LYRICS_PROVIDER_NAME for p in self.providers])
        return ("Couldn't find lyrics for '%s' by %s. <br><br>Tried the following lyrics providers: %s" % (song, artist, providerlist), None)


    def generateCache(self):
        for i in range(self.totalsongs):
            if self.quitting: break
            artist = self.songdata["playlist"][i]["a"].encode("utf8")
            song = self.songdata["playlist"][i]["t"].encode("utf8")
            self.emit(QtCore.SIGNAL("cachegenProgressUpdate"), i+1, song, artist)
            QApplication.processEvents()
            if self.lyricsCacheRef.checkSong(song, artist) is False:
                lyrics, lyricsprovidername = self.getUpdatedLyrics(song, artist)
                if lyricsprovidername is not None:
                    self.emit(QtCore.SIGNAL("print"), "Updated cached lyrics for '%s' by %s from %s" % (song, artist, lyricsprovidername))
                elif lyrics is not None:
                    #Couldnt find lyrics. lyrics holds the error message.
                    self.emit(QtCore.SIGNAL("print"), lyrics.replace("<br>", ""))
            #else:
            #    self.emit(QtCore.SIGNAL("print"), "Lyrics for '%s' by %s are already cached." % (song, artist))
            #Qt will crash if we overload it with signals so this just throttles it a bit, not noticeable to end user
            sleep(0.001)
        self.emit(QtCore.SIGNAL("cacheGenerationComplete"))
        self.emit(QtCore.SIGNAL("workFinished()"))


class CacheBuilder(object):
    def __init__(self, songdata, progressbar_widget, lyricsCacheRef, lyricsProviderRef):
        self.cacheBuilderThread = None
        self.cacheBuilderWorkTask = None
        self.lyricsCacheRef = lyricsCacheRef
        self.lyricsProvidersRef = lyricsProviderRef
        self.progressbar_widget = progressbar_widget
        self.totalsongs = len(songdata["playlist"])
        self.songdata = songdata
        self.dialog = QApplication.activeWindow().window()

    def cancelBuild(self):
        self.killThread()
        self.dialog.close()

    def killThread(self):
        if self.cacheBuilderThread is not None:
            self.cacheBuilderWorkTask.quitting = True
            self.cacheBuilderThread.quit()
            self.cacheBuilderThread.wait()
            if self.cacheBuilderWorkTask is not None:
                QtCore.QObject.disconnect(self.cacheBuilderThread, QtCore.SIGNAL("started()"), self.cacheBuilderWorkTask.generateCache)

    def updateProgress(self, i, song, artist):
        perc = (float(i)/self.totalsongs)*100
        labeltext = "[%s/%s - %.1f%%] Updating cached lyrics for '%s' by %s" % (i, self.totalsongs, perc, song, artist)
        self.progressbar_widget.progressLabel.setText(labeltext)
        self.progressbar_widget.progressBar.setValue(i)
        QtGui.QApplication.processEvents()

    #Printing inside the QThread is dangerous because of the way we have set up our print output to go to a QTextEdit
    @staticmethod
    def printCallback(s):
        print s
        QtGui.QApplication.processEvents()

    def generationFinished(self):
        print "Done generating cache files."
        #Get a main-window reference
        for w in QApplication.topLevelWidgets():
            if isinstance(w, QtGui.QMainWindow):
                mainwindow = w
        QtGui.QMessageBox.information(mainwindow, "Cache Generation Complete", "Finished generating cache files. Check the console tab for for additional information.", QtGui.QMessageBox.Ok)
        self.dialog.close()

    def startCacheGeneration(self):
        self.progressbar_widget.progressBar.setMaximum(self.totalsongs)
        self.killThread()

        self.cacheBuilderThread = QtCore.QThread()
        self.cacheBuilderWorkTask = threadedCacheGenerator(self.songdata, self.lyricsCacheRef, self.lyricsProvidersRef)
        self.cacheBuilderWorkTask.moveToThread(self.cacheBuilderThread)

        QtCore.QObject.connect(self.cacheBuilderThread, QtCore.SIGNAL("started()"), self.cacheBuilderWorkTask.generateCache)
        QtCore.QObject.connect(self.cacheBuilderWorkTask, QtCore.SIGNAL("cacheGenerationComplete"), self.generationFinished)
        QtCore.QObject.connect(self.cacheBuilderWorkTask, QtCore.SIGNAL("workFinished()"), self.cacheBuilderThread.quit)
        QtCore.QObject.connect(self.cacheBuilderWorkTask, QtCore.SIGNAL("cachegenProgressUpdate"), self.updateProgress)
        QtCore.QObject.connect(self.cacheBuilderWorkTask, QtCore.SIGNAL("print"), self.printCallback)
        self.cacheBuilderThread.start()
