# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lyrics_search_dialog.ui'
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

class closableDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(closableDialog, self).__init__(parent)
    def closeEvent(self, QCloseEvent):
        self.emit(QtCore.SIGNAL("SearchDialogClosing"))
        QCloseEvent.accept()


class Ui_lyricsSearchDialog(object):
    def setupUi(self, lyricsSearchDialog):
        self.widget = lyricsSearchDialog
        lyricsSearchDialog.setObjectName(_fromUtf8("lyricsSearchDialog"))
        lyricsSearchDialog.resize(600, 600)
        lyricsSearchDialog.setMinimumSize(QtCore.QSize(600, 600))
        self.horizontalLayout = QtGui.QHBoxLayout(lyricsSearchDialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.leftFrame = QtGui.QFrame(lyricsSearchDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftFrame.sizePolicy().hasHeightForWidth())
        self.leftFrame.setSizePolicy(sizePolicy)
        self.leftFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.leftFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.leftFrame.setObjectName(_fromUtf8("leftFrame"))
        self.verticalLayout = QtGui.QVBoxLayout(self.leftFrame)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.leftGroupBox_Controls = QtGui.QGroupBox(self.leftFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.leftGroupBox_Controls.sizePolicy().hasHeightForWidth())
        self.leftGroupBox_Controls.setSizePolicy(sizePolicy)
        self.leftGroupBox_Controls.setObjectName(_fromUtf8("leftGroupBox_Controls"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.leftGroupBox_Controls)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.songNameInput = QtGui.QLineEdit(self.leftGroupBox_Controls)
        self.songNameInput.setFrame(True)
        self.songNameInput.setObjectName(_fromUtf8("songNameInput"))
        self.verticalLayout_2.addWidget(self.songNameInput)
        self.artistNameInput = QtGui.QLineEdit(self.leftGroupBox_Controls)
        self.artistNameInput.setObjectName(_fromUtf8("artistNameInput"))
        self.verticalLayout_2.addWidget(self.artistNameInput)
        self.lyricsSearchStringInput = QtGui.QLineEdit(self.leftGroupBox_Controls)
        self.lyricsSearchStringInput.setObjectName(_fromUtf8("lyricsSearchStringInput"))
        self.verticalLayout_2.addWidget(self.lyricsSearchStringInput)
        self.searchButton = QtGui.QPushButton(self.leftGroupBox_Controls)
        self.searchButton.setObjectName(_fromUtf8("searchButton"))
        self.verticalLayout_2.addWidget(self.searchButton)
        self.verticalLayout.addWidget(self.leftGroupBox_Controls)
        self.leftTabWidget_Results = QtGui.QTabWidget(self.leftFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.leftTabWidget_Results.sizePolicy().hasHeightForWidth())
        self.leftTabWidget_Results.setSizePolicy(sizePolicy)
        self.leftTabWidget_Results.setTabsClosable(True)
        self.leftTabWidget_Results.setObjectName(_fromUtf8("leftTabWidget_Results"))
        self.verticalLayout.addWidget(self.leftTabWidget_Results)
        self.horizontalLayout.addWidget(self.leftFrame)
        self.resultLyricsView = QtGui.QTextEdit(lyricsSearchDialog)
        self.resultLyricsView.setAcceptRichText(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resultLyricsView.sizePolicy().hasHeightForWidth())
        self.resultLyricsView.setSizePolicy(sizePolicy)
        self.resultLyricsView.setObjectName(_fromUtf8("resultLyricsView"))
        self.horizontalLayout.addWidget(self.resultLyricsView)

        self.retranslateUi(lyricsSearchDialog)
        lyricsSearchDialog.setTabOrder(self.songNameInput, self.artistNameInput)
        lyricsSearchDialog.setTabOrder(self.artistNameInput, self.lyricsSearchStringInput)
        lyricsSearchDialog.setTabOrder(self.lyricsSearchStringInput, self.searchButton)
        lyricsSearchDialog.setTabOrder(self.searchButton, self.leftTabWidget_Results)
        lyricsSearchDialog.setTabOrder(self.leftTabWidget_Results, self.resultLyricsView)

    def retranslateUi(self, lyricsSearchDialog):
        lyricsSearchDialog.setWindowTitle(_translate("lyricsSearchDialog", "Dialog", None))
        self.songNameInput.setPlaceholderText(_translate("lyricsSearchDialog", "Song Name (or part of)", None))
        self.artistNameInput.setPlaceholderText(_translate("lyricsSearchDialog", "Artist Name (or part of)", None))
        self.lyricsSearchStringInput.setPlaceholderText(_translate("lyricsSearchDialog", "Lyrics Search String", None))
        self.searchButton.setText(_translate("lyricsSearchDialog", "Search Lyrics Cache", None))

