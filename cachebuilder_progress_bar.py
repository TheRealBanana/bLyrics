# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cachebuilder_progress_bar.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
from time import sleep
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
    def setupUi(self, cachebuilderProgressDialog, songdata, getLyricsFunc, lyricsCacheRef):
        self.totalsongs = len(songdata["playlist"])
        self.songdata = songdata
        self.getLyricsFunc = getLyricsFunc
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
        QtCore.QMetaObject.connectSlotsByName(cachebuilderProgressDialog)

    def cancelBuild(self):
        self.quit = True
        self.widget.close()

    def generateCache(self):
        i = 0
        self.progressBar.setMaximum(self.totalsongs)
        QtGui.QApplication.processEvents()
        try:
            while self.quit == False and i < self.totalsongs:
                #Update the progress bar
                artist = self.songdata["playlist"][i]["a"].encode("utf8")
                song = self.songdata["playlist"][i]["t"].encode("utf8")
                perc = (float(i)/self.totalsongs)*100
                labeltext = "[%s/%s - %.1f%%] Updating cached lyrics for '%s' by %s" % (i, self.totalsongs, perc, song, artist)
                self.progressLabel.setText(labeltext)
                self.progressBar.setValue(i)
                QtGui.QApplication.processEvents()
                i += 1
                #And get then update the song lyrics. Skip songs already in the cache.
                if self.lyricsCacheRef.checkSong(song, artist) is False:
                    lyrics = self.getLyricsFunc(song, artist, forced=True)
                    try:
                        lyrics = lyrics.encode("utf8")
                    except:
                        pass
                    try:
                        self.lyricsCacheRef.saveLyrics(song, artist, str(lyrics))
                    except:
                        print "There was an error saving lyrics for '%s' by %s. Skipping this song..." % (song, artist)
                        continue
                else:
                    print "Lyrics for '%s' by %s are already cached." % (song, artist)
                QtGui.QApplication.processEvents()
        except Exception as e:
            print "Cache generation halted due to an error: "
            print e
        print "Done generating cache files."
        self.widget.close()

    def retranslateUi(self, cachebuilderProgressDialog):
        cachebuilderProgressDialog.setWindowTitle(_translate("cachebuilderProgressDialog", "Dialog", None))
        self.progressLabel.setText(_translate("cachebuilderProgressDialog", "Building cache...", None))
        self.cancelButton.setText(_translate("cachebuilderProgressDialog", "Cancel", None))

