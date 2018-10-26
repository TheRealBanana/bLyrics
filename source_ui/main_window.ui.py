# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
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
        spacerItem = QtGui.QSpacerItem(433, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 1, 1, 1, 1)
        self.RefreshLyricsButton = QtGui.QPushButton(self.LyricsTab)
        self.RefreshLyricsButton.setObjectName(_fromUtf8("RefreshLyricsButton"))
        self.gridLayout_3.addWidget(self.RefreshLyricsButton, 1, 0, 1, 1)
        self.lyricsTextView = QtGui.QTextBrowser(self.LyricsTab)
        self.lyricsTextView.setObjectName(_fromUtf8("lyricsTextView"))
        self.gridLayout_3.addWidget(self.lyricsTextView, 0, 0, 1, 2)
        self.RefreshLyricsButton.raise_()
        self.lyricsTextView.raise_()
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
        self.actionDisconnect = QtGui.QAction(MainWindow)
        self.actionDisconnect.setObjectName(_fromUtf8("actionDisconnect"))
        self.actionReconnect = QtGui.QAction(MainWindow)
        self.actionReconnect.setObjectName(_fromUtf8("actionReconnect"))
        self.actionClearCache = QtGui.QAction(MainWindow)
        self.actionClearCache.setObjectName(_fromUtf8("actionClearCache"))
        self.actionOptions = QtGui.QAction(MainWindow)
        self.actionOptions.setObjectName(_fromUtf8("actionOptions"))
        self.menuFile.addAction(self.actionReconnect)
        self.menuFile.addAction(self.actionDisconnect)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClearCache)
        self.menuFile.addAction(self.actionOptions)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.aboutMenuItem)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QObject.connect(self.RefreshLyricsButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.close)
        QtCore.QObject.connect(self.tabWidget, QtCore.SIGNAL(_fromUtf8("currentChanged(int)")), self.MainStatusWebView.reload)
        QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QObject.connect(self.consoleO_ClearButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "bLyrics", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.MainTab), _translate("MainWindow", "Current Status", None))
        self.RefreshLyricsButton.setText(_translate("MainWindow", "Refresh", None))
        self.lyricsTextView.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">asdf</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.LyricsTab), _translate("MainWindow", "Lyrics", None))
        self.consoleO_ClearButton.setText(_translate("MainWindow", "Clear", None))
        self.consoleOutput.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">REDIRECT_STDOUT_HERE</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ConsoleTab), _translate("MainWindow", "Console", None))
        self.Statusbar.setText(_translate("MainWindow", "<p style=\"color: blue;\">STATUSBAR WITH BENEFITS...... CSS BENEFITS!</p>", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.aboutMenuItem.setText(_translate("MainWindow", "About", None))
        self.actionQuit.setText(_translate("MainWindow", "Quit", None))
        self.actionDisconnect.setText(_translate("MainWindow", "Disconnect", None))
        self.actionReconnect.setText(_translate("MainWindow", "Reconnect", None))
        self.actionClearCache.setText(_translate("MainWindow", "Clear playlist cache", None))
        self.actionOptions.setText(_translate("MainWindow", "Options", None))

from PyQt4 import QtWebKit
import icon_resource_rc
