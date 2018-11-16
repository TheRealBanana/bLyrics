# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'manualQueryDialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

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

class Ui_customQueryDialog(object):
    def setupUi(self, customQueryDialog):
        customQueryDialog.setObjectName(_fromUtf8("customQueryDialog"))
        customQueryDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        customQueryDialog.resize(280, 130)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(customQueryDialog.sizePolicy().hasHeightForWidth())
        customQueryDialog.setSizePolicy(sizePolicy)
        customQueryDialog.setMinimumSize(QtCore.QSize(280, 130))
        customQueryDialog.setMaximumSize(QtCore.QSize(280, 130))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icon/bLyrics.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        customQueryDialog.setWindowIcon(icon)
        customQueryDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(customQueryDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.mainFrame = QtGui.QFrame(customQueryDialog)
        self.mainFrame.setFrameShape(QtGui.QFrame.Box)
        self.mainFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.mainFrame.setObjectName(_fromUtf8("mainFrame"))
        self.gridLayout_2 = QtGui.QGridLayout(self.mainFrame)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.artistLabel = QtGui.QLabel(self.mainFrame)
        self.artistLabel.setObjectName(_fromUtf8("artistLabel"))
        self.gridLayout_2.addWidget(self.artistLabel, 0, 0, 1, 1)
        self.artistEntryText = QtGui.QLineEdit(self.mainFrame)
        self.artistEntryText.setObjectName(_fromUtf8("artistEntryText"))
        self.gridLayout_2.addWidget(self.artistEntryText, 0, 1, 1, 1)
        self.songTitleLabel = QtGui.QLabel(self.mainFrame)
        self.songTitleLabel.setObjectName(_fromUtf8("songTitleLabel"))
        self.gridLayout_2.addWidget(self.songTitleLabel, 1, 0, 1, 1)
        self.songTitleEntryText = QtGui.QLineEdit(self.mainFrame)
        self.songTitleEntryText.setObjectName(_fromUtf8("songTitleEntryText"))
        self.gridLayout_2.addWidget(self.songTitleEntryText, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.mainFrame, 0, 0, 1, 1)
        self.submitCancelbuttons = QtGui.QDialogButtonBox(customQueryDialog)
        self.submitCancelbuttons.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.submitCancelbuttons.setOrientation(QtCore.Qt.Horizontal)
        self.submitCancelbuttons.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.submitCancelbuttons.setCenterButtons(True)
        self.submitCancelbuttons.setObjectName(_fromUtf8("submitCancelbuttons"))
        self.gridLayout.addWidget(self.submitCancelbuttons, 1, 0, 1, 1)
        self.artistLabel.setBuddy(self.artistEntryText)
        self.songTitleLabel.setBuddy(self.songTitleEntryText)

        self.retranslateUi(customQueryDialog)
        QtCore.QObject.connect(self.submitCancelbuttons, QtCore.SIGNAL(_fromUtf8("accepted()")), customQueryDialog.accept)
        QtCore.QObject.connect(self.submitCancelbuttons, QtCore.SIGNAL(_fromUtf8("rejected()")), customQueryDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(customQueryDialog)
        customQueryDialog.setTabOrder(self.artistEntryText, self.songTitleEntryText)
        customQueryDialog.setTabOrder(self.songTitleEntryText, self.submitCancelbuttons)

    def retranslateUi(self, customQueryDialog):
        customQueryDialog.setWindowTitle(_translate("customQueryDialog", "Manual lyrics query", None))
        self.artistLabel.setText(_translate("customQueryDialog", "Artist:", None))
        self.songTitleLabel.setText(_translate("customQueryDialog", "Song Title:", None))

