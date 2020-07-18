# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'blyrics_ui.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(550, 650)
        MainWindow.setMinimumSize(QtCore.QSize(550, 650))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icon/bLyrics.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.MainTab = QtGui.QWidget()
        self.MainTab.setObjectName(_fromUtf8("MainTab"))
        self.gridLayout_2 = QtGui.QGridLayout(self.MainTab)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.MainStatusWebView = QtWebKit.QWebView(self.MainTab)
        self.MainStatusWebView.setUrl(QtCore.QUrl(_fromUtf8("http://192.168.2.130:8888/ajquery/index.html")))
        self.MainStatusWebView.setObjectName(_fromUtf8("MainStatusWebView"))
        self.gridLayout_2.addWidget(self.MainStatusWebView, 0, 0, 1, 1)
        self.tabWidget.addTab(self.MainTab, _fromUtf8(""))
        self.LyricsTab = QtGui.QWidget()
        self.LyricsTab.setObjectName(_fromUtf8("LyricsTab"))
        self.gridLayout_3 = QtGui.QGridLayout(self.LyricsTab)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.lyricsTextView = QtGui.QTextBrowser(self.LyricsTab)
        self.lyricsTextView.setUndoRedoEnabled(True)
        self.lyricsTextView.setObjectName(_fromUtf8("lyricsTextView"))
        self.gridLayout_3.addWidget(self.lyricsTextView, 0, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(433, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 1, 2, 1, 1)
        self.editLyricsButton = QtGui.QPushButton(self.LyricsTab)
        self.editLyricsButton.setObjectName(_fromUtf8("editLyricsButton"))
        self.gridLayout_3.addWidget(self.editLyricsButton, 1, 1, 1, 1)
        self.RefreshLyricsButton = QtGui.QPushButton(self.LyricsTab)
        self.RefreshLyricsButton.setObjectName(_fromUtf8("RefreshLyricsButton"))
        self.gridLayout_3.addWidget(self.RefreshLyricsButton, 1, 0, 1, 1)
        self.RefreshLyricsButton.raise_()
        self.lyricsTextView.raise_()
        self.editLyricsButton.raise_()
        self.tabWidget.addTab(self.LyricsTab, _fromUtf8(""))
        self.ConsoleTab = QtGui.QWidget()
        self.ConsoleTab.setObjectName(_fromUtf8("ConsoleTab"))
        self.gridLayout_4 = QtGui.QGridLayout(self.ConsoleTab)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.consoleO_ClearButton = QtGui.QPushButton(self.ConsoleTab)
        self.consoleO_ClearButton.setObjectName(_fromUtf8("consoleO_ClearButton"))
        self.gridLayout_4.addWidget(self.consoleO_ClearButton, 1, 0, 1, 1)
        self.consoleOutput = QtGui.QTextBrowser(self.ConsoleTab)
        self.consoleOutput.setObjectName(_fromUtf8("consoleOutput"))
        self.gridLayout_4.addWidget(self.consoleOutput, 0, 0, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(424, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 1, 1, 1, 1)
        self.tabWidget.addTab(self.ConsoleTab, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.Statusbar = QtGui.QLabel(self.centralwidget)
        self.Statusbar.setTextFormat(QtCore.Qt.AutoText)
        self.Statusbar.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.Statusbar.setObjectName(_fromUtf8("Statusbar"))
        self.gridLayout.addWidget(self.Statusbar, 2, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(1, 3, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 550, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.aboutMenuItem = QtGui.QAction(MainWindow)
        self.aboutMenuItem.setObjectName(_fromUtf8("aboutMenuItem"))
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionOptions = QtGui.QAction(MainWindow)
        self.actionOptions.setObjectName(_fromUtf8("actionOptions"))
        self.actionRefresh = QtGui.QAction(MainWindow)
        self.actionRefresh.setObjectName(_fromUtf8("actionRefresh"))
        self.actionSearchLyrics = QtGui.QAction(MainWindow)
        self.actionSearchLyrics.setObjectName(_fromUtf8("actionSearchLyrics"))
        self.actionClearLyricsCache = QtGui.QAction(MainWindow)
        self.actionClearLyricsCache.setObjectName(_fromUtf8("actionClearLyricsCache"))
        self.actionPregenLyricsCache = QtGui.QAction(MainWindow)
        self.actionPregenLyricsCache.setObjectName(_fromUtf8("actionPregenLyricsCache"))
        self.actionConvertOldCache = QtGui.QAction(MainWindow)
        self.actionConvertOldCache.setObjectName(_fromUtf8("actionConvertOldCache"))
        self.menuFile.addAction(self.actionRefresh)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOptions)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSearchLyrics)
        self.menuFile.addAction(self.actionClearLyricsCache)
        self.menuFile.addAction(self.actionPregenLyricsCache)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.aboutMenuItem)
        self.menuHelp.addAction(self.actionConvertOldCache)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.tabWidget, self.MainStatusWebView)
        MainWindow.setTabOrder(self.MainStatusWebView, self.lyricsTextView)
        MainWindow.setTabOrder(self.lyricsTextView, self.RefreshLyricsButton)
        MainWindow.setTabOrder(self.RefreshLyricsButton, self.editLyricsButton)
        MainWindow.setTabOrder(self.editLyricsButton, self.consoleOutput)
        MainWindow.setTabOrder(self.consoleOutput, self.consoleO_ClearButton)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "bLyrics", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.MainTab), _translate("MainWindow", "Current Status", None))
        self.lyricsTextView.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">_LYRICS_DISPLAY_</span></p></body></html>", None))
        self.editLyricsButton.setText(_translate("MainWindow", "Edit", None))
        self.RefreshLyricsButton.setText(_translate("MainWindow", "Refresh", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.LyricsTab), _translate("MainWindow", "Lyrics", None))
        self.consoleO_ClearButton.setText(_translate("MainWindow", "Clear", None))
        self.consoleOutput.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">_STDOUT_STRERR_OUTPUT_</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ConsoleTab), _translate("MainWindow", "Console", None))
        self.Statusbar.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#0000ff;\">_CSS_STATUS_BAR_</span></p></body></html>", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.aboutMenuItem.setText(_translate("MainWindow", "About", None))
        self.actionQuit.setText(_translate("MainWindow", "Quit", None))
        self.actionOptions.setText(_translate("MainWindow", "Options", None))
        self.actionRefresh.setText(_translate("MainWindow", "Refresh Lyrics", None))
        self.actionSearchLyrics.setText(_translate("MainWindow", "Search Lyrics Cache", None))
        self.actionClearLyricsCache.setText(_translate("MainWindow", "Clear Lyrics Cache", None))
        self.actionPregenLyricsCache.setText(_translate("MainWindow", "Generate Lyrics Cache", None))
        self.actionConvertOldCache.setText(_translate("MainWindow", "Convert old cache to new format", None))

from PyQt4 import QtWebKit
import icon_resource_rc
