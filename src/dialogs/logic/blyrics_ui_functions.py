from ..about_pane import Ui_aboutWindow
from ..options_dialog import Ui_OptionsDialog
from ..generic_progress_bar import Ui_genericProgressDialog
from ..lyrics_search_dialog import Ui_lyricsSearchDialog
from options_dialog_functions import optionsDialogFunctions
from cachebuilder import CacheBuilder
from lyrics_search_functions import lyricsSearchFunctions
from foobarhttpcontrol import foobarStatusDownloader
from lyrics_downloader import threadedLyricsDownloader
from lyrics_cacher import LyricsCacher
from PyQt4 import QtCore, QtGui
from time import time as tTime
from datetime import datetime as dTime
from re import split as REsplit
from re import sub as REsub

from sys import exit as sys_exit


#To force this program to always be on top of other windows change this to True
_ALWAYS_ON_TOP_ = False

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
        self.emit(QtCore.SIGNAL("ClosableDialogClosing"))
        QCloseEvent.accept()


class UIFunctions(object):
    def __init__(self, UiReference):
        self.UI = UiReference
        self.optionsWindowui = Ui_OptionsDialog()
        self.optionsWindowFunctionsInstance = None
        self.searchWidget = None
        self.searchfunctionsinstance = None
        self.windowTitle = None
        self.timer = None
        self.is_connected = False
        self.actual_song = ""
        self.last_song = None
        self.lyricsCache = LyricsCacher()
#        self.lyricsCache.preloadLyricsCacheIntoMemory()
        self.lyricsDownloader = None
        self.lyricsDownloaderThread = None
        self.cacheBuilder = None
        self.address = ("127.0.0.1", 8888)
        self.fb2k = foobarStatusDownloader(UiReference.MainWindow, self.address)
        self.last_sb_message = None
        #Set up the name of our app and the company name for saving settings later
        #We also tell it to save as an INI file in %APPDATA% (the default location)
        self.appSettings = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, "Kylesplace.org", "bLyrics2")
        self.loadedOptions = {}
        self.webStatus_URL = ""
        #Some default settings for the appearance
        self.fontStyle = 'MS Shell Dlg 2, 8'
        self.fontFgColor = '#000000'
        self.fontBgColor = '#FFFFFF'
        self.masterMatchRatio = 0.65

    #Rewriting this app is daunting to say the least. I am making a new main function with the hopes
    #of just replacing the old crappy main function with better code bit by bit.
    ##
    #In terms of how this app functions, our main app loop is run by a QTimer defined in blyrics_ui.py.
    #This timer is executed every 5 seconds, ostensibly to check whether our song has changed or not but
    #its evolved to do quite a bit more over time. Hopefully I can cut out the cruft.
    def mainAppLoop(self):

        return_data = self.fb2k.getStatus()

        if return_data is not None:
            self.actual_song = return_data["song_name"]
            self.actual_artist = return_data["artist_name"]

            if return_data["song_name"] is not None:
                songartist = "%s - %s" % (return_data["song_name"], return_data["artist_name"])
            else:
                songartist = self.last_song

            #Status bar update
            if int(return_data["playback_mode"]) == 0 and return_data["next_song_in_playlist"] is not None:
                songinfotxt = "Next Song: %s" % return_data["next_song_in_playlist"]
            else:
                songinfotxt = "Current Song: %s" % songartist
            self.setStatusbarText("%s" % songinfotxt)
            #Window title update
            if int(return_data["isplaying"]) or int(return_data["ispaused"]):
                self.setWindowTitle("bLyrics  ::  %s  ::  %s" % (["Playing","Paused"][int(return_data["ispaused"])], songartist))
            else:
                self.setWindowTitle("bLyrics  ::  Stopped  ::  %s" % songartist)

            self.getUpdatedLyrics(return_data["song_name"], return_data["artist_name"])

    def getUpdatedLyrics(self, song, artist, forced=False):
        if self.hasSongChanged() or forced:
            if self.lyricsCache.checkSong(song, artist) is True:
                cachedlyrics = self.lyricsCache.getLyrics(song, artist)
                if len(cachedlyrics) > 0:
                    print "Returned cached lyrics for '%s' by %s" % (song, artist)
                    self.setLyricsText(cachedlyrics)
                    return
                else:
                    print "Zero length lyrics cache file, trying to grab fresh lyrics..."
            self.createNewThreadWork(song, artist)


    def createNewThreadWork(self, song, artist):
        self.setLyricsText("Retrieving lyrics...")
        if self.lyricsDownloaderThread is not None:
            if self.lyricsDownloaderThread.isFinished() is True:
                self.lyricsDownloaderThread.quit()
            else:
                if self.lyricsDownloaderThread.isRunning() is True:
                    return None
                self.lyricsDownloaderThread.quit()
            #Make sure
            self.lyricsDownloaderThread.wait()
            QtCore.QObject.disconnect(self.lyricsDownloaderThread, QtCore.SIGNAL("started()"), self.lyricsWorkTask.doWork)

        self.lyricsDownloaderThread = QtCore.QThread()
        self.lyricsWorkTask = threadedLyricsDownloader(song, artist)
        self.lyricsWorkTask.moveToThread(self.lyricsDownloaderThread)

        QtCore.QObject.connect(self.lyricsDownloaderThread, QtCore.SIGNAL("started()"), self.lyricsWorkTask.doWork)
        QtCore.QObject.connect(self.lyricsWorkTask, QtCore.SIGNAL("workFinished()"), self.lyricsDownloaderThread.quit)
        QtCore.QObject.connect(self.lyricsWorkTask, QtCore.SIGNAL("lyricsUpdate"), self.updateLyricsFromThread)
        self.lyricsDownloaderThread.start()

    def updateLyricsFromThread(self, lyrics, lyricsprovidername):
        if lyricsprovidername is not None:
            print "Retrieved lyrics for '%s' by %s from %s" % (self.actual_song, self.actual_artist, lyricsprovidername)
        else:
            #If lyricsprovidername is None we error'd out and the lyrics var holds our error message
            print lyrics.replace("<br>", "")
        self.setLyricsText(lyrics)

    def hasSongChanged(self):
        if self.last_song == self.actual_song:
            return False
        else:
            self.last_song = self.actual_song
            return True

    def openOptionsWindow(self):
        widget = QtGui.QDialog()
        self.optionsWindowui.setupUi(widget)
        optionsfunctions = optionsDialogFunctions(widget, self)

        if _ALWAYS_ON_TOP_:
            widget.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        widget.setWindowIcon(QtGui.QIcon(":/icon/bLyrics.ico"))
        widget.exec_()
        #Refresh the UI with the updated options
        self.refreshLyricsButtonAction()
        #Not necessary.... probably
        del optionsfunctions

    def openAboutWindow(self):
        #self.widget = QtGui.QWidget()
        self.widget = QtGui.QDialog()
        self.aboutWindowui = Ui_aboutWindow()
        self.aboutWindowui.setupUi(self.widget)
        self.widget.setWindowIcon(QtGui.QIcon(":/icon/bLyrics.ico"))
        #self.widget.show()
        #Set the window to be always on top if always-on-top is enabled
        if _ALWAYS_ON_TOP_:
            self.widget.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.widget.exec_()

    def saveSettings(self, data):
        #Ok we are receiving data from the options menu.
        #Data is in the same structure used in loadSettings()
        self.appSettings.beginGroup("Options")
        for subGroup in data:
            self.appSettings.beginGroup(subGroup)
            #start stuffing data in
            for key,val in data[subGroup].iteritems():
                self.appSettings.setValue(key, val)
            #End the group and get to the next one
            self.appSettings.endGroup()

        #Now that we're done iterating over the data we can sync it and finish
        self.appSettings.endGroup()
        self.loadedOptions = data
        #Now we update the Ui
        self.setupUiOptions()

    def saveWindowState(self):
        #Begin group for basic app settings
        self.appSettings.beginGroup("WindowState")
        #Screen size and position
        self.appSettings.setValue("windowSize", self.UI.MainWindow.size())
        self.appSettings.setValue("windowPos", self.UI.MainWindow.pos())
        self.appSettings.endGroup()
        self.appSettings.sync()
        #Not a great place to put this but while we're here....
        if self.lyricsDownloaderThread is not None:
            self.lyricsDownloaderThread.quit()
            self.lyricsDownloaderThread.wait(1000)

    def quitApp(self):
        self.saveWindowState()
        sys_exit(0)

    def testSettingGroup(self, groupName):
        if self.appSettings.childGroups().contains(groupName):
                return True
        else:
            return False

    def loadSettings(self):
        global _ALWAYS_ON_TOP_ #need to remove this in the future, global vars are not great

        #Start with a clean slate
        self.loadedOptions = {}

        #Check if we have any options, if not set up some defaults.
        #We dont care about the window state since that will be set on close anyway.
        if self.appSettings.childGroups().contains("Options") is False:
            #Set up default options
            self.loadedOptions = {
                'Appearance':
                    {'fgFontColor': '#000000', 'bgFontColor': '#FFFFFF', 'fontNameAndSize': 'Tahoma, 8'},
                'Advanced':
                    {'alwaysOnTop': False, 'debugModeEnabled': False, 'debugWriteEnabled': False, 'masterMatchRatio': '0.65', 'debugOutputFolder': '.'},
                'fb2kServerInfo':
                    {'userpassreq': False, 'user': '', 'pass': '', 'port': '8888', 'address': '127.0.0.1'}}
        else:
            #Retrieve all saved settings
            self.appSettings.beginGroup("Options")

            #Our settings are contained in a series of subgroups
            for subGroup in self.appSettings.childGroups():
                #Because we are going to be saving this for later use in normal python code
                #we are going to convert all QStrings to python strings to be safe.
                subGroup = str(subGroup)
                self.appSettings.beginGroup(subGroup)
                self.loadedOptions[subGroup] = {}

                #And get our settings for this group
                for key in self.appSettings.childKeys():
                    #Again we dont want the QString
                    key = str(key)
                    value = self.appSettings.value(key)
                    #Convert our QVariant into its appropriate data type
                    if value.type() == QtCore.QMetaType.QString:
                        value = str(value.toPyObject())
                        #Fix true/false stuff
                        if value == "true": value = True
                        elif value == "false": value = False
                    elif value.type() == QtCore.QMetaType.QStringList:
                        value = str(value.toPyObject().join(";")).split(";")

                    self.loadedOptions[subGroup][key] = value
                self.appSettings.endGroup()

            self.appSettings.endGroup()

        #Load last window position/size if we have it available
        if self.appSettings.childGroups().contains("WindowState") is True:
            self.appSettings.beginGroup("WindowState")
            self.UI.MainWindow.resize(self.appSettings.value("windowSize").toSize())
            self.UI.MainWindow.move(self.appSettings.value("windowPos").toPoint())
            self.appSettings.endGroup()

        _ALWAYS_ON_TOP_ = self.loadedOptions["Advanced"]["alwaysOnTop"]

        #Finally apply our settings to the UI
        self.setupUiOptions()



    def setupUiOptions(self):
        #Set the templates installed
        self.address = (self.loadedOptions["fb2kServerInfo"]["address"], self.loadedOptions["fb2kServerInfo"]["port"])
        self.webStatus_URL = "http://"
        #Set up the options we've been given

        #First we set the status page url with the given info.
        #Credentials
        if self.loadedOptions["fb2kServerInfo"]["userpassreq"] is True: self.webStatus_URL += "%s:%s@" % (self.loadedOptions["fb2kServerInfo"]["user"], self.loadedOptions["fb2kServerInfo"]["pass"])
        #IP and port
        self.webStatus_URL += "%s:%s/ajquery/index.html" % (self.loadedOptions["fb2kServerInfo"]["address"], self.loadedOptions["fb2kServerInfo"]["port"])

        #Set the URL
        self.UI.MainStatusWebView.setUrl(QtCore.QUrl(_fromUtf8(self.webStatus_URL)))

        #Now we set the user-defined appearance settings.
        self.fontStyle = self.loadedOptions["Appearance"]["fontNameAndSize"]
        self.fontBgColor = self.loadedOptions["Appearance"]["bgFontColor"]
        self.fontFgColor = self.loadedOptions["Appearance"]["fgFontColor"]

        #Now on to the advanced page
        lwop = {}
        #Set the debug mode/write mode
        lwop["debugModeEnabled"] = self.loadedOptions["Advanced"]["debugModeEnabled"]
        lwop["debugWriteEnabled"] = self.loadedOptions["Advanced"]["debugWriteEnabled"]
        lwop["debugOutputFolder"] = self.loadedOptions["Advanced"]["debugOutputFolder"]
        lwop["masterMatchRatio"] = self.loadedOptions["Advanced"]["masterMatchRatio"]
        self.masterMatchRatio = lwop["masterMatchRatio"]

    def clear_console(self):
        html = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
</style></head><body style=" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"></p></body></html>
'''
        self.UI.consoleOutput.setHtml(_translate("MainWindow", html, None))

    def write(self, text):
        #This function allows us to set stderr and stdout to write to this function instead of the usual output.
        #That way any time a print or error occurs it will be output to this function, which will write to the console tab.
        if text.strip() != "":
            timestamp = dTime.fromtimestamp(tTime()).strftime('%d/%b/%Y-%I:%M:%S %p:   ')
            text = timestamp + text + "\n"
            #Set our cursor to the bottom of the console so we scroll with the output, but only if we are already scrolled to the bottom
            #I hate it when I'm trying to read the output of someone program and it resets on a new output.
            #If the user is scrolled all the way down keep scrolling down, otherwise dont update
            #Need to get the console output vertical scrollbar reference
            vscrollbar = self.UI.consoleOutput.verticalScrollBar()
            scrollmax = vscrollbar.maximum()
            scrollval = vscrollbar.value()
            #Cursor infos incase we have a selection we want to preserve
            cursor = self.UI.consoleOutput.textCursor()
            cursorstart = cursor.selectionStart()
            cursorend = cursor.selectionEnd()

            #Insert text at the very bottom
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.insertText(text)

            #did we have any text selection we should preserve?
            if cursorstart != cursorend:
                cursor.setPosition(cursorstart, QtGui.QTextCursor.MoveAnchor)
                cursor.setPosition(cursorend, QtGui.QTextCursor.KeepAnchor)
                self.UI.consoleOutput.setTextCursor(cursor)

            #close enough for government work!
            if scrollmax - scrollval < 5:
                self.UI.consoleOutput.verticalScrollBar().setSliderPosition(self.UI.consoleOutput.verticalScrollBar().maximum())
            elif scrollval != 0:
                self.UI.consoleOutput.verticalScrollBar().setSliderPosition(scrollval)

            self.UI.consoleOutput.setFocus()

    def setWindowTitle(self, text):
        self.UI.MainWindow.setWindowTitle(_translate("MainWindow", text, None))
        self.windowTitle = text

    def setLyricsText(self, lyrics):
        if lyrics is not None and isinstance(lyrics, basestring):
            fontFamily, size = REsplit(",", self.fontStyle)
            fontFamily = str(fontFamily).strip()
            fontSize = str(size).strip()
            #Remove href, img, and div tags from the lyrics
            lyrics = REsub("</?a( .*?)?>", "", lyrics)
            lyrics = REsub("</?div( .*?)?>", "", lyrics)
            lyrics = REsub("</?img( .*?)?>", "", lyrics)
            html = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
</style></head><body style="color: %s; background-color: %s; font-family:\'%s\'; font-size:%spt; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">%s</p></body></html>
''' % (self.fontFgColor, self.fontBgColor, fontFamily, fontSize, lyrics)
            self.UI.lyricsTextView.setHtml(_translate("MainWindow", html, None))

    def setStatusbarText(self, text):
        if text is not None and len(text) > 0:
            self.UI.Statusbar.setText(_translate("MainWindow", text, None))

    def areYouSureQuestion(self, title, message):
        return QtGui.QMessageBox.question(self.UI.MainWindow, title, message, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

    def clearLyricsCacheAction(self):
        #U sure?
        if  self.areYouSureQuestion("Clear Lyrics Cache?", "<p align='center'>Are you sure you want to remove all %s cached lyrics?<br>(This cannot be undone)</p>" % self.lyricsCache.getCacheSize()) == QtGui.QMessageBox.Yes:
            numfiles = self.lyricsCache.clearLyricsCache()
            QtGui.QMessageBox.information(self.UI.MainWindow, "Cached Cleared!", "Successfully cleared %s cached lyrics files!" % numfiles)
            print "Removed %d cached lyrics" % numfiles

    def refreshLyricsButtonAction(self):
        self.last_song = None
        self.mainAppLoop()

    def editLyricsButtonAction(self):
        self.UI.lyricsTextView.setReadOnly(False)
        self.UI.lyricsTextView.setFocus()
        self.UI.lyricsTextView.selectAll()

        #Repurpose our old refresh and edit buttons into save and cancel buttons
        QtCore.QObject.disconnect(self.UI.RefreshLyricsButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.refreshLyricsButtonAction)
        QtCore.QObject.disconnect(self.UI.editLyricsButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.editLyricsButtonAction)
        self.UI.RefreshLyricsButton.setText("Save")
        QtCore.QObject.connect(self.UI.RefreshLyricsButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.saveEditedLyrics)
        self.UI.editLyricsButton.setText("Cancel")
        QtCore.QObject.connect(self.UI.editLyricsButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.resetEditLyricsState)

    def saveEditedLyrics(self):
        newlyrics = unicode(self.UI.lyricsTextView.toPlainText())
        #If we get a blank page (i.e. no lyrics) we reacquire lyrics from online sources
        #If the user really wants to have no lyrics (blank page) they can put a space or line break.
        self.lyricsCache.saveLyrics(self.actual_song, self.actual_artist, newlyrics.encode("utf8"))
        print "Saved updated lyrics for '%s' by %s" % (self.actual_song, self.actual_artist)
        self.resetEditLyricsState()


    def resetEditLyricsState(self):
        #Undo everything done by editLyricsButtonAction()
        if not self.UI.lyricsTextView.isReadOnly():
            #Deselect any text and move cursor to the top
            cursor = self.UI.lyricsTextView.textCursor()
            cursor.clearSelection()
            cursor.movePosition(QtGui.QTextCursor.Start)
            self.UI.lyricsTextView.setTextCursor(cursor)
            self.UI.lyricsTextView.setReadOnly(True)
            #Repurpose our old refresh and edit buttons into save and cancel buttons
            QtCore.QObject.disconnect(self.UI.RefreshLyricsButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.saveEditedLyrics)
            QtCore.QObject.disconnect(self.UI.editLyricsButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.resetEditLyricsState)
            self.UI.RefreshLyricsButton.setText("Refresh")
            QtCore.QObject.connect(self.UI.RefreshLyricsButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.refreshLyricsButtonAction)
            self.UI.editLyricsButton.setText("Edit")
            QtCore.QObject.connect(self.UI.editLyricsButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.editLyricsButtonAction)
            self.refreshLyricsButtonAction()

    def pregenLyricsCache(self):
        #Find out the current number of songs in the active playlist
        oldpagelength = self.fb2k.queryWebInterface()["playlistItemsPerPage"]
        #Hope the user doesn't have more than 16384 songs in a single playlist
        try:
            songdata = self.fb2k.queryWebInterface(urlsuffix="/ajquery/?cmd=PlaylistItemsPerPage&param1=16384&param3=js/state.json")
        except:
            return
        #Switch back no matter what happens
        finally:
            self.fb2k.queryWebInterface(urlsuffix="/ajquery/?cmd=PlaylistItemsPerPage&param1=%s&param3=js/state.json" % oldpagelength, noreturn=True)
        totalsongs = len(songdata["playlist"])


        #This is going to take a whole lot of time so we are going to display a progress bar w/ a cancel button.
        #Make sure the user knows whats up
        title = "Pregenerate lyrics?"
        message = "<p align='center'>Are you sure you want to download lyrics for all %s songs in the current playlist?<br><br>(This will take a while but can be canceled)</p>" % totalsongs
        if self.areYouSureQuestion(title, message) == QtGui.QMessageBox.No: return

        widget = QtGui.QDialog(self.UI.MainWindow)
        cachebuilderui = Ui_genericProgressDialog()
        cachebuilderui.setupUi(widget)
        QtCore.QObject.connect(widget, QtCore.SIGNAL("cacheGenerationComplete"), self.cacheBuildReturn)
       # widget.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        widget.setWindowIcon(QtGui.QIcon(":/icon/bLyrics.ico"))
        widget.setWindowTitle("Pre-Generating Cache Files...")
        #widget.setModal(True)
        widget.show()
        if self.cacheBuilder is not None:
            del self.cacheBuilder
        self.cacheBuilder = CacheBuilder(songdata, cachebuilderui)
        self.cacheBuilder.startCacheGeneration()

    def cacheBuildReturn(self):
        print "Done generating cache files."
        QtGui.QMessageBox.information(self.UI.MainWindow, "Cache Generation Complete", "Finished generating cache files. Check the console tab for for additional information.", QtGui.QMessageBox.Ok)

    def searchLyricsAction(self):
        #Cant search if we dont have our cache loaded so check that first
        if self.lyricsCache.loadedIntoMem is False:
            self.loadLyricsCacheIntoMemory()
            if self.lyricsCache.loadedIntoMem is False: #User canceled build
                QtGui.QMessageBox.critical(self.UI.MainWindow, "Cache Load Canceled", "Cannot search lyrics without preloading lyrics into memory.", QtGui.QMessageBox.Ok)
                return

        #Not sure if this is the right way to do it but I'm going with it for now
        if self.searchWidget is not None:
            self.searchWidget.deleteLater()
            self.searchWidget = None
            self.searchfunctionsinstance = None
        self.searchWidget = closableDialog()
        searchdialog = Ui_lyricsSearchDialog()
        searchdialog.setupUi(self.searchWidget)
        self.searchfunctionsinstance = lyricsSearchFunctions(searchdialog, self.lyricsCache)
        if _ALWAYS_ON_TOP_:
            self.searchWidget.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        QtCore.QObject.connect(self.searchWidget, QtCore.SIGNAL("ClosableDialogClosing"), self.searchfunctionsinstance.closeDialog)
        self.searchWidget.setWindowIcon(QtGui.QIcon(":/icon/bLyrics.ico"))
        self.searchWidget.setWindowTitle("Search Lyrics Cache")
        searchdialog.searchButton.setFocus()
        self.searchWidget.show()

    def loadLyricsCacheIntoMemory(self):
        #widget = QtGui.QDialog(self.UI.MainWindow)
        widget = closableDialog(self.UI.MainWindow)
        preloaderui = Ui_genericProgressDialog()
        preloaderui.setupUi(widget)
        QtCore.QObject.connect(widget, QtCore.SIGNAL("ClosableDialogClosing"), self.lyricsCache.cancelPreload)
        widget.setWindowIcon(QtGui.QIcon(":/icon/bLyrics.ico"))
        widget.setWindowTitle("Cache Preloading...")
        widget.show()
        self.lyricsCache.preloadLyricsCacheIntoMemory(preloaderui)
        widget.close()

