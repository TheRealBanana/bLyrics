# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cachebuilder_progress_bar.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
from logic.lyrics_cacher import LyricsCacher
from PyQt4 import QtCore, QtGui
from logic.lyricsProviders import lyricswiki, songlyrics
provider_classes = [lyricswiki.LyricsProvider, songlyrics.LyricsProvider]


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class threadedCacheGenerator(QtCore.QObject):
    def __init__(self, songdata):
        self.songdata = songdata
        self.totalsongs = len(self.songdata["playlist"])
        self.quitting = False
        self.lyricsCacheRef = LyricsCacher()
        self.providers = [p() for p in provider_classes]
        super(threadedCacheGenerator, self).__init__()

    def getUpdatedLyrics(self, song, artist):
        #Check our cache, and download if missing
        for p in self.providers:
            if self.quitting is True: return None, None
            lyrics = p.getLyrics(song, artist)
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
        i = 0
        while self.quitting is False and i < self.totalsongs:
            artist = self.songdata["playlist"][i]["a"].encode("utf8")
            song = self.songdata["playlist"][i]["t"].encode("utf8")
            self.emit(QtCore.SIGNAL("cachegenProgressUpdate"), i, song, artist)
            if self.lyricsCacheRef.checkSong(song, artist) is False:
                lyrics, lyricsprovidername = self.getUpdatedLyrics(song, artist)
                if lyricsprovidername is not None:
                    self.emit(QtCore.SIGNAL("print"), "Updated cached lyrics for '%s' by %s from %s" % (song, artist, lyricsprovidername))
                elif lyrics is not None:
                    #Couldnt find lyrics
                    self.emit(QtCore.SIGNAL("print"), lyrics.replace("<br>", ""))
            else:
                self.emit(QtCore.SIGNAL("print"), "Lyrics for '%s' by %s are already cached." % (song, artist))
            i += 1

        self.emit(QtCore.SIGNAL("cacheGenerationComplete"))


class Ui_cachebuilderProgressDialog(object):
    def __init__(self):
        self.cacheBuilderThread = None
        self.cacheBuilderWorkTask = None
        super(Ui_cachebuilderProgressDialog, self).__init__()

    def setupUi(self, cachebuilderProgressDialog, songdata):
        self.totalsongs = len(songdata["playlist"])
        self.songdata = songdata
        self.widget = cachebuilderProgressDialog
        cachebuilderProgressDialog.setObjectName(_fromUtf8("cachebuilderProgressDialog"))
        cachebuilderProgressDialog.resize(450, 123)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(cachebuilderProgressDialog.sizePolicy().hasHeightForWidth())
        cachebuilderProgressDialog.setSizePolicy(sizePolicy)
        cachebuilderProgressDialog.setMinimumSize(QtCore.QSize(298, 123))
        cachebuilderProgressDialog.setMaximumSize(QtCore.QSize(16777215, 123))
        self.verticalLayout = QtGui.QVBoxLayout(cachebuilderProgressDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.progressBar = QtGui.QProgressBar(cachebuilderProgressDialog)
        self.progressBar.setTextVisible(False)
        self.progressBar.setFormat(_fromUtf8("%p%"))
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.progressLabel = QtGui.QLabel(cachebuilderProgressDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressLabel.sizePolicy().hasHeightForWidth())
        self.progressLabel.setWordWrap(True)
        self.progressLabel.setSizePolicy(sizePolicy)
        self.progressLabel.setMinimumSize(QtCore.QSize(280, 0))
        self.progressLabel.setMaximumSize(QtCore.QSize(1500, 16777215))
        self.progressLabel.setTextFormat(QtCore.Qt.PlainText)
        self.progressLabel.setObjectName(_fromUtf8("progressLabel"))
        self.verticalLayout.addWidget(self.progressLabel)
        self.centeredCancelButton = QtGui.QFrame(cachebuilderProgressDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centeredCancelButton.sizePolicy().hasHeightForWidth())
        self.centeredCancelButton.setSizePolicy(sizePolicy)
        self.centeredCancelButton.setMinimumSize(QtCore.QSize(205, 40))
        self.centeredCancelButton.setMaximumSize(QtCore.QSize(16777215, 40))
        self.centeredCancelButton.setObjectName(_fromUtf8("centeredCancelButton"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centeredCancelButton)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cancelButton = QtGui.QPushButton(self.centeredCancelButton)
        self.cancelButton.setMinimumSize(QtCore.QSize(75, 22))
        self.cancelButton.setMaximumSize(QtCore.QSize(75, 22))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        spacerItem1 = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.centeredCancelButton)

        self.retranslateUi(cachebuilderProgressDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.cancelBuild)
        QtCore.QMetaObject.connectSlotsByName(cachebuilderProgressDialog)

    def cancelBuild(self):
        self.killThread()
        self.widget.close()

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
        self.progressLabel.setText(labeltext)
        self.progressBar.setValue(i)
        QtGui.QApplication.processEvents()

    #Printing inside the QThread is dangerous because of the way we have set up our print output to go to a QTextEdit
    @staticmethod
    def printCallback(s):
        print s

    #Signal bucket brigade, only for the most pr0 coders ofc
    def generationFinished(self):
        self.widget.emit(QtCore.SIGNAL("cacheGenerationComplete"))

    def startCacheGeneration(self):
        self.progressBar.setMaximum(self.totalsongs)
        self.killThread()

        self.cacheBuilderThread = QtCore.QThread()
        self.cacheBuilderWorkTask = threadedCacheGenerator(self.songdata)
        self.cacheBuilderWorkTask.moveToThread(self.cacheBuilderThread)

        QtCore.QObject.connect(self.cacheBuilderThread, QtCore.SIGNAL("started()"), self.cacheBuilderWorkTask.generateCache)
        QtCore.QObject.connect(self.cacheBuilderWorkTask, QtCore.SIGNAL("cacheGenerationComplete"), self.generationFinished)
        QtCore.QObject.connect(self.cacheBuilderWorkTask, QtCore.SIGNAL("workFinished()"), self.cacheBuilderThread.quit)
        QtCore.QObject.connect(self.cacheBuilderWorkTask, QtCore.SIGNAL("cachegenProgressUpdate"), self.updateProgress)
        QtCore.QObject.connect(self.cacheBuilderWorkTask, QtCore.SIGNAL("print"), self.printCallback)
        self.cacheBuilderThread.start()

    def retranslateUi(self, cachebuilderProgressDialog):
        cachebuilderProgressDialog.setWindowTitle(_translate("cachebuilderProgressDialog", "Pre-Generating Cache Files...", None))
        self.progressLabel.setText(_translate("cachebuilderProgressDialog", "Building cache...", None))
        self.cancelButton.setText(_translate("cachebuilderProgressDialog", "Cancel", None))

