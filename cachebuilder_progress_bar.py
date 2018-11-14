# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cachebuilder_progress_bar.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
from time import sleep
from lyrics_downloader import threadedLyricsDownloader
from PyQt4 import QtCore, QtGui

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

class Ui_cachebuilderProgressDialog(object):
    def __init__(self):
        self.song = None
        self.artist = None
        self.i = 0
        self.lyricsDownloaderThread = None
        self.lyricsWorkTask = None
        super(Ui_cachebuilderProgressDialog, self).__init__()

    def setupUi(self, cachebuilderProgressDialog, songdata, lyricsCacheRef):
        self.totalsongs = len(songdata["playlist"])
        self.songdata = songdata
        self.lyricsCacheRef = lyricsCacheRef
        self.quit = False
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
        QtCore.QObject.connect(self.widget, QtCore.SIGNAL("alreadyInCache"), self.cacheUpdateReturn)
        QtCore.QObject.connect(self.widget, QtCore.SIGNAL("nextIteration"), self.nextIteration)
        QtCore.QMetaObject.connectSlotsByName(cachebuilderProgressDialog)

    def cancelBuild(self):
        self.quit = True
        self.killThread()
        self.widget.close()

    #Run it as a state machine
    #Give it the songlist and an internal i
    #Initiate download and stop
    #When download finishes it releases a signal
    #Signal hits a function in this class that does:
    #   Save Lyrics to Cache
    #   Increment i
    #   Launch new thread
    #   Wait some more and repeat

    def killThread(self):
        if self.lyricsDownloaderThread is not None:
            self.lyricsDownloaderThread.quit()
            self.lyricsDownloaderThread.wait()
            QtCore.QObject.disconnect(self.lyricsDownloaderThread, QtCore.SIGNAL("started()"), self.lyricsWorkTask.doWork)

    def updateSongArtist(self, song, artist):
        self.song = song
        self.artist = artist

    def updateProgress(self):
        perc = (float(self.i)/self.totalsongs)*100
        labeltext = "[%s/%s - %.1f%%] Updating cached lyrics for '%s' by %s" % (self.i, self.totalsongs, perc, self.song, self.artist)
        self.progressLabel.setText(labeltext)
        self.progressBar.setValue(self.i)
        QtGui.QApplication.processEvents()

    def cacheUpdateReturn(self, lyrics, lyricsprovidername):
        if lyrics is not None and lyricsprovidername is not None:
            print "Updated cached lyrics for '%s' by %s from %s" % (self.song, self.artist, lyricsprovidername)
            try:
                lyrics = lyrics.encode("utf8")
            except:
                pass
            try:
                self.lyricsCacheRef.saveLyrics(self.song, self.artist, lyrics)
            except:
                print "There was an error saving lyrics for '%s' by %s. Skipping this song..." % (self.song, self.artist)
        self.i += 1
        self.widget.emit(QtCore.SIGNAL("nextIteration"))

    def nextIteration(self):
        if self.quit == False and self.i < self.totalsongs:
            self.artist = self.songdata["playlist"][self.i]["a"].encode("utf8")
            self.song = self.songdata["playlist"][self.i]["t"].encode("utf8")
            self.updateProgress()
            if self.lyricsCacheRef.checkSong(self.song, self.artist) is False:
                self.createNewThreadWork()
            else:
                print "Lyrics for '%s' by %s are already cached." % (self.song, self.artist)
                self.widget.emit(QtCore.SIGNAL("alreadyInCache"), None, None)
        else:
            print "Done generating cache files."
            self.widget.emit(QtCore.SIGNAL("cacheGenerationComplete"))

    def createNewThreadWork(self):
        self.killThread()

        self.lyricsDownloaderThread = QtCore.QThread()
        self.lyricsWorkTask = threadedLyricsDownloader(self.song, self.artist)
        self.lyricsWorkTask.moveToThread(self.lyricsDownloaderThread)

        QtCore.QObject.connect(self.lyricsDownloaderThread, QtCore.SIGNAL("started()"), self.lyricsWorkTask.doWork)
        QtCore.QObject.connect(self.lyricsWorkTask, QtCore.SIGNAL("workFinished()"), self.lyricsDownloaderThread.quit)
        QtCore.QObject.connect(self.lyricsWorkTask, QtCore.SIGNAL("lyricsUpdate"), self.cacheUpdateReturn)
        self.lyricsDownloaderThread.start()

    def startCacheGeneration(self):
        self.i = 0
        self.progressBar.setMaximum(self.totalsongs)

    def retranslateUi(self, cachebuilderProgressDialog):
        cachebuilderProgressDialog.setWindowTitle(_translate("cachebuilderProgressDialog", "Dialog", None))
        self.progressLabel.setText(_translate("cachebuilderProgressDialog", "Building cache...", None))
        self.cancelButton.setText(_translate("cachebuilderProgressDialog", "Cancel", None))

