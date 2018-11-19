# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from logic.blyrics_ui_functions import *
from PyQt4 import QtGui
from PyQt4 import QtWebKit
from icon_resource_rc import *

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
    def __init__(self, MainWindow):
        #Stuff needed before setupUi
        self.MainWindow = MainWindow
        self.UiFunctions = UIFunctions(self)

    def setupUi(self):
        #just a few class globals
        ##Setting up the GUI, most of this was autogenerated by Qt Designer
        self.MainWindow.setObjectName(_fromUtf8("MainWindow"))
        self.MainWindow.resize(559, 673)
        self.MainWindow.setMinimumSize(QtCore.QSize(550, 650))
        #Set the icon
        self.MainWindow.setWindowIcon(QtGui.QIcon(":/icon/bLyrics.ico"))
        self.centralwidget = QtGui.QWidget(self.MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.MainTab = QtGui.QWidget()
        self.MainTab.setObjectName(_fromUtf8("MainTab"))
        self.gridLayout_2 = QtGui.QGridLayout(self.MainTab)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.MainStatusWebView = QtWebKit.QWebView(self.MainTab)
        self.MainStatusWebView.setObjectName(_fromUtf8("MainStatusWebView"))
        self.gridLayout_2.addWidget(self.MainStatusWebView, 0, 0, 1, 1)
        self.tabWidget.addTab(self.MainTab, _fromUtf8(""))
        self.LyricsTab = QtGui.QWidget()
        self.LyricsTab.setObjectName(_fromUtf8("LyricsTab"))
        #lyrics tab context menu
        self.LyricsTab.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        ######
        self.gridLayout_3 = QtGui.QGridLayout(self.LyricsTab)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.lyricsTextView = QtGui.QTextEdit(self.LyricsTab)
        self.lyricsTextView.setObjectName(_fromUtf8("lyricsTextView"))
        self.lyricsTextView.setReadOnly(True)
        self.gridLayout_3.addWidget(self.lyricsTextView, 0, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(433, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 1, 2, 1, 1)
        self.RefreshLyricsButton = QtGui.QPushButton(self.LyricsTab)
        self.RefreshLyricsButton.setObjectName(_fromUtf8("RefreshLyricsButton"))
        self.gridLayout_3.addWidget(self.RefreshLyricsButton, 1, 0, 1, 1)
        self.editLyricsButton = QtGui.QPushButton(self.LyricsTab)
        self.editLyricsButton.setObjectName(_fromUtf8("editLyricsButton"))
        self.gridLayout_3.addWidget(self.editLyricsButton, 1, 1, 1, 1)
        self.RefreshLyricsButton.raise_()
        self.lyricsTextView.raise_()
        self.editLyricsButton.raise_()
        self.tabWidget.addTab(self.LyricsTab, _fromUtf8(""))

        self.ConsoleTab = QtGui.QWidget()
        self.ConsoleTab.setObjectName(_fromUtf8("ConsoleTab"))
        self.gridLayout_4 = QtGui.QGridLayout(self.ConsoleTab)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.consoleOutput = QtGui.QTextBrowser(self.ConsoleTab)
        self.virtScrollBar = self.consoleOutput.verticalScrollBar()
        self.consoleOutput.setObjectName(_fromUtf8("consoleOutput"))
        self.gridLayout_4.addWidget(self.consoleOutput, 0, 0, 1, 2)
        self.consoleO_ClearButton = QtGui.QPushButton(self.ConsoleTab)
        self.consoleO_ClearButton.setObjectName(_fromUtf8("consoleO_ClearButton"))
        self.gridLayout_4.addWidget(self.consoleO_ClearButton, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(424, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 1, 1, 1, 1)

        self.tabWidget.addTab(self.ConsoleTab, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        #Our new QLabel statusbar
        self.Statusbar = QtGui.QLabel(self.centralwidget)
        statusBarFont = QtGui.QFont()
        statusBarFont.setFamily(_fromUtf8("Segoe UI"))
        statusBarFont.setPointSize(9)
        statusBarFont.setKerning(False)
        self.Statusbar.setFont(statusBarFont)
        self.Statusbar.setTextFormat(QtCore.Qt.AutoText)
        self.Statusbar.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.Statusbar.setObjectName(_fromUtf8("Statusbar"))
        self.gridLayout.addWidget(self.Statusbar, 2, 0, 1, 1)
        statusbarSpacer = QtGui.QSpacerItem(1, 4, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(statusbarSpacer, 1, 0, 1, 1)

        self.MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 559, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.MainWindow.setMenuBar(self.menubar)
        self.aboutMenuItem = QtGui.QAction(self.MainWindow)
        self.aboutMenuItem.setObjectName(_fromUtf8("aboutMenuItem"))
        self.menuHelp.addAction(self.aboutMenuItem)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.actionRefresh = QtGui.QAction(self.MainWindow)
        self.actionRefresh.setObjectName(_fromUtf8("actionRefresh"))

        self.actionQuit = QtGui.QAction(self.MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))

        self.actionOptions = QtGui.QAction(self.MainWindow)
        self.actionOptions.setObjectName(_fromUtf8("actionOptions"))

        self.actionClearLyricsCache = QtGui.QAction(self.MainWindow)
        self.actionClearLyricsCache.setObjectName(_fromUtf8("actionClearLyricsCache"))

        self.actionPregenLyricsCache = QtGui.QAction(self.MainWindow)
        self.actionPregenLyricsCache.setObjectName(_fromUtf8("actionPregenLyricsCache"))


        #Build file menu
        self.menuFile.addAction(self.actionRefresh)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOptions)
        self.menuFile.addAction(self.actionClearLyricsCache)
        self.menuFile.addAction(self.actionPregenLyricsCache)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)

        #Build help menu
        self.menuHelp.addAction(self.aboutMenuItem)

        self.retranslateUi()
        self.tabWidget.setCurrentIndex(1)   #This sets the default tab, starting from 0 = current status tab, 1 = lyrics tab, and 2 = console

        #Load up settings the user saved such as window position, web interface url, debug mode, etc
        self.UiFunctions.loadSettings()

        #Set up our slot connections
        QtCore.QObject.connect(self.RefreshLyricsButton, QtCore.SIGNAL("clicked()"), self.UiFunctions.refreshLyricsButtonAction)
        QtCore.QObject.connect(self.editLyricsButton, QtCore.SIGNAL("clicked()"), self.UiFunctions.editLyricsButtonAction)
        QtCore.QObject.connect(self.tabWidget, QtCore.SIGNAL(_fromUtf8("currentChanged(int)")), self.MainStatusWebView.reload)
        QtCore.QObject.connect(self.aboutMenuItem, QtCore.SIGNAL(_fromUtf8("triggered()")), self.UiFunctions.openAboutWindow)
        QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL(_fromUtf8("triggered()")), self.MainWindow.close)
        QtCore.QObject.connect(self.actionRefresh, QtCore.SIGNAL(_fromUtf8("triggered()")), self.UiFunctions.mainAppLoop)
        QtCore.QObject.connect(self.actionOptions, QtCore.SIGNAL(_fromUtf8("triggered()")), self.UiFunctions.openOptionsWindow)
        QtCore.QObject.connect(self.actionClearLyricsCache, QtCore.SIGNAL(_fromUtf8("triggered()")), self.UiFunctions.clearLyricsCacheAction)
        QtCore.QObject.connect(self.actionPregenLyricsCache, QtCore.SIGNAL(_fromUtf8("triggered()")), self.UiFunctions.pregenLyricsCache)
        QtCore.QObject.connect(self.consoleO_ClearButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.UiFunctions.clear_console)
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)


        #Tab order
        self.MainWindow.setTabOrder(self.tabWidget, self.MainStatusWebView)
        self.MainWindow.setTabOrder(self.MainStatusWebView, self.lyricsTextView)
        self.MainWindow.setTabOrder(self.lyricsTextView, self.RefreshLyricsButton)
        self.MainWindow.setTabOrder(self.RefreshLyricsButton, self.editLyricsButton)
        self.MainWindow.setTabOrder(self.editLyricsButton, self.consoleOutput)
        self.MainWindow.setTabOrder(self.consoleOutput, self.consoleO_ClearButton)

        #Tell the user we're not connected
        self.UiFunctions.setLyricsText("Not connected to Foobar2000's Web server, press check your settings and make sure Foobar is running.")
        self.UiFunctions.setWindowTitle("bLyrics  ::  Not Connected - Press Refresh or Connect")
        self.UiFunctions.setStatusbarText("Foobar2000 Web Interface Not Found")
        self.UiFunctions.write("bLyrics Started")

        #Set up the internal loop that checks for a new song and retrieves lyrics when needed.
        if self.UiFunctions.timer is None:
            self.UiFunctions.timer = QtCore.QTimer()
            QtCore.QObject.connect(self.UiFunctions.timer, QtCore.SIGNAL("timeout()"), self.UiFunctions.mainAppLoop)
        self.UiFunctions.timer.start(5000)
        #And now we just manually execute the check_song_loop ourselves the first time instead of waiting 5s for the first iteration of the timer to finish.
        self.UiFunctions.mainAppLoop()

    def retranslateUi(self):
        self.UiFunctions.setWindowTitle("bLyrics  ::  Not Connected")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.MainTab), _translate("MainWindow", "Current Status", None))
        self.RefreshLyricsButton.setText(_translate("MainWindow", "Refresh", None))
        self.editLyricsButton.setText(_translate("MainWindow", "Edit", None))
        self.UiFunctions.setLyricsText("No Song Playing or Program Not Setup Properly")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.LyricsTab), _translate("MainWindow", "Lyrics", None))
        self.consoleOutput.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\"></span></p></body></html>", None))
        self.consoleO_ClearButton.setText(_translate("MainWindow", "Clear", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ConsoleTab), _translate("MainWindow", "Console", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.aboutMenuItem.setText(_translate("MainWindow", "About", None))
        self.actionQuit.setText(_translate("MainWindow", "Quit", None))
        self.actionRefresh.setText(_translate("MainWindow", "Refresh Lyrics", None))
        self.actionOptions.setText(_translate("MainWindow", "Options", None))
        self.actionClearLyricsCache.setText(_translate("MainWindow", "Clear Lyrics Cache", None))
        self.actionPregenLyricsCache.setText(_translate("MainWindow", "Generate Lyrics Cache", None))
        self.Statusbar.setText(_translate("MainWindow", "Welcome to bLyrics", None))


