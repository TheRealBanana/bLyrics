import urllib2
import json
import re
from about_pane import *
from options_dialog import *
from manualQueryDialog import *
from lyricswiki import lyricswikiObj
from PyQt4 import QtCore, QtGui
from time import time as tTime
from datetime import datetime as dTime
from re import split as REsplit
from re import sub as REsub


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

#Downloads the current song/artist/playmode from foobar's ajquery web interface
class foobarStatusDownloader(object):
    def __init__(self, MWref, hostnameandport):
        self.MWref = MWref
        self.address = hostnameandport[0]
        self.port = hostnameandport[1]

    def queryWebInterface(self, urlsuffix="/ajquery/?param3=js/state.json", noreturn=False):
        try:
            page = urllib2.urlopen("http://" + str(self.address) + ":" + str(self.port) + str(urlsuffix))
            if noreturn:
                return None
            rawjson = page.read()
            page.close()
            data = json.loads(rawjson)
        except:
            return None
        return data


    def getStatus(self):
        data = self.queryWebInterface()

        if data is None:
            print "Connection error of some sort"
            return None

        isplaying = int(data["isPlaying"])
        ispaused = int(data["isPaused"])
        playback_mode = int(data["playbackOrder"])

        if isplaying or ispaused:
            current_song_id = int(data["playingItem"])
        else:
            #Currently stopped so try and use either the last playing song or the currently focused item
            if len(data["prevplayedItem"]) > 0:
                current_song_id = int(data["prevplayedItem"])
            else:
                try:
                    current_song_id = int(data["focusedItem"])
                except:
                    current_song_id = "?"

        #Deriving the page ourselves because playlistPage is just whatever page is currently visible, not the page
        #that our song is actually on.
        if (data["playlistActive"] == data["playlistPlaying"]) or data["playingItem"] == "?" and current_song_id != "?":
            current_page = (current_song_id/int(data["playlistItemsPerPage"])) + 1
            cur_position_on_page = current_song_id - (current_page-1) * int(data["playlistItemsPerPage"])
            current_song_name = data["playlist"][cur_position_on_page]["t"]
            current_artist = data["playlist"][cur_position_on_page]["a"]
            try:
                next_song_in_playlist = data["playlist"][cur_position_on_page+1]["t"] + " - " + data["playlist"][cur_position_on_page+1]["a"]
            except:
                next_song_in_playlist = None
        else:
            if len(data["helper1"]) > 0:
                #Not on the correct playlist page, fall back to less reliable helperi fields
                current_song_name = re.match("^(.*) - $", data["helper1"]).group(1)
                current_artist = re.search("(.*) - %s" % re.escape(current_song_name), data["helper2"]).group(1)
                next_song_in_playlist = None
            else:
                return None

        return_data = {}
        return_data["isplaying"] = isplaying
        return_data["ispaused"] = ispaused
        return_data["playback_mode"] = playback_mode
        return_data["song_name"] = current_song_name.encode("utf8")
        return_data["artist_name"] = current_artist.encode("utf8")
        return_data["next_song_in_playlist"] = next_song_in_playlist
        return return_data


class UIFunctions(object):
    def __init__(self, UiReference):
        self.UI = UiReference
        self.optionsWindowui = Ui_OptionsDialog()
        self.output = [dTime.fromtimestamp(tTime()).strftime('%d/%b/%Y-%I:%M:%S %p:   ') + "PROGRAM_INIT"]
        self.windowTitle = None
        self.timer = None
        self.is_connected = False
        self.actual_song = ""
        self.last_song = None
        self.lyricsProg = lyricswikiObj(self)
        self.address = ("127.0.0.1", 8888)
        self.fb2k = foobarStatusDownloader(UiReference.MainWindow, self.address)
        self.last_sb_message = None
        #Set up the name of our app and the company name for saving settings later
        #We also tell it to save as an INI file in %APPDATA% (the default location)
        self.appSettings = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, "Kylesplace.org", "bLyrics2")
        #Need this to load options without excess code
        self.optionsWindowui = Ui_OptionsDialog()
        self.webStatus_URL = ""
        #Some default settings for the appearance
        self.fontStyle = 'MS Shell Dlg 2, 8'
        self.fontFgColor = '#000000'
        self.fontBgColor = '#FFFFFF'

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


            #Finally update the lyrics. Our manual and search modes really make this more complicated than it should be.
            if self.lyricsProg.manual_mode["manual"] is True:
                if self.lyricsProg.manual_mode["song_at_set"] != self.actual_song:
                    self.lyricsProg.manual_mode["man"] = False
                    self.lyricsProg.update_current_track(return_data["song_name"], return_data["artist_name"])
            else:
                self.lyricsProg.update_current_track(return_data["song_name"], return_data["artist_name"])
            lyrics = self.lyricsProg.getLyrics()
            if lyrics is not None:
                self.resetEditLyricsState()
                self.setLyricsText(lyrics)

    def hasSongChanged(self):
        if self.last_song == self.actual_song:
            return False
        else:
            self.last_song = self.actual_song
            return True

    def openOptionsWindow(self):
        widget = QtGui.QDialog()
        self.optionsWindowui.setupUi(widget, self, _ALWAYS_ON_TOP_)
        if _ALWAYS_ON_TOP_:
            widget.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        widget.setWindowIcon(QtGui.QIcon(":/icon/bLyrics.ico"))
        widget.exec_()

    def openSearchDialog(self):
        #Set tab to the search output before we do anything
        self.UI.tabWidget.setCurrentIndex(1)
        widget = QtGui.QDialog()
        mQDialog = Ui_customQueryDialog()
        return_data = []
        mQDialog.setupUi(widget, return_data)
        if _ALWAYS_ON_TOP_:
            widget.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        widget.setWindowTitle(_translate("customQueryDialog", "Search for lyrics", None))
        widget.setWindowIcon(QtGui.QIcon(":/icon/bLyrics.ico"))
        widget.exec_()
        #change to normal python strings
        if len(return_data) > 0:
            return_data = [str(z) for z in return_data]

        #Now we get the first page of results in the form of a list where each item is a dictionary with three parts: Artist, Song Title, and URL.
        if len(return_data) > 0:
            search_results = self.lyricsProg.searchForLyrics(song=return_data[1], artist=return_data[0])
        else:
            search_results = ""
        if len(search_results) > 0:
            result_html_template = '''
<p style="font-weight: normal; font-family: Tahoma, Geneva, sans-serif; font-size: 18px; font-weight: bold;">%s)<a href="%s"><span style="font-size: 14px;"> %s <span style="font-weight: normal;">by</span> %s</span></a></p>'''
            html_body = ""
            #We make an HTML page containing all the results for the user to select from.
            #First we build up the body of our html using result_html as a template
            for index, result_entry in enumerate(search_results):
                combined_url = "#%s::%s::%s" % (result_entry["url"], result_entry["title"], result_entry["artist"])
                html_body += result_html_template % (index+1, combined_url, result_entry["title"], result_entry["artist"])
            #Now we generate the main html
            main_html = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><title>Search Results</title></head><body><p style="font-family: Tahoma, Geneva, sans-serif; font-weight: bold; font-size: 24px;">%s LYRIC RESULTS:</p>
%s
</body></html>''' % (len(search_results), html_body)
            #And now we display the output to the user in the lyrics tab
            self.UI.lyricsTextView.setHtml(_translate("MainWindow", main_html, None))

    def resetManualEntry(self):
        self.lyricsProg.resetManualEntry()
        self.mainAppLoop()

    def setSearchResult(self, url):
        self.lyricsProg.manual_url_set(str(url.toString()[1:])) # cut off the beginning hash
        self.mainAppLoop()

    def openManualQueryDialog(self):
        widget = QtGui.QDialog()
        mQDialog = Ui_customQueryDialog()
        return_data = []
        mQDialog.setupUi(widget, return_data)
        if _ALWAYS_ON_TOP_:
            widget.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        widget.setWindowTitle(_translate("customQueryDialog", "Manual lyrics query", None))
        widget.setWindowIcon(QtGui.QIcon(":/icon/bLyrics.ico"))
        widget.exec_()
        #change to normal python strings
        return_data = [str(z) for z in return_data]
        #Now we need to let fooBarLyrics.py know we have a manual query so it doesnt just change the song back when it senses the change
        if len(return_data) > 0:
            self.lyricsProg.manual_song_set(return_data)
            #Now force the mainUI to update
            self.mainAppLoop()


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

    def saveSettings(self, optionsMenu=False, data=[]):
        #This will just go ahead and save everything unless told not to
        if optionsMenu is True:
            #Ok we are receiving data from the options menu.
            #The data list is a list of three dictionaries, each one holding
            #settings from its respective page. Index 0 being the first page
            #and so-on.
            self.appSettings.beginGroup("Options")
            for index in xrange(len(data)):
                #Begin the appropriate group
                if index == 0:
                    self.appSettings.beginGroup("Appearance")
                if index == 1:
                    self.appSettings.beginGroup("fb2kServerInfo")
                if index == 2:
                    self.appSettings.beginGroup("Advanced")

                #start stuffing data in
                for key,val in data[index].iteritems():
                    self.appSettings.setValue(key, val)

                #End the group and get to the next one
                self.appSettings.endGroup()

            #Now that we're done iterating over the data we can sync it and finish
            self.appSettings.endGroup()
            #Now we update the Ui
            optionsdict = {}
            optionsdict["Appearance"] = [data[0]["fontNameAndSize"], data[0]["bgFontColor"], data[0]["fgFontColor"]]
            optionsdict["fb2kServerInfo"] = [data[1]["address"], data[1]["port"], data[1]["userpassreq"], data[1]["user"], data[1]["pass"]]
            optionsdict["Advanced"] = [data[2]["debugModeEnabled"], data[2]["debugWriteEnabled"], data[2]["debugOutputFolder"], data[2]["masterMatchRatio"], data[2]["alwaysOnTop"]]
            self.setupUiOptions(optionsdict)

        #Begin group for basic app settings
        self.appSettings.beginGroup("WindowState")
        #Screen size and position
        self.appSettings.setValue("windowSize", self.UI.MainWindow.size())
        self.appSettings.setValue("windowPos", self.UI.MainWindow.pos())
        self.appSettings.endGroup()
        self.appSettings.sync()

    def testSettingGroup(self, groupName):
        #The reason we join() and then split() is because it's a quick way to convert a QStringList,
        #containing a bunch of QStrings, all into a single string at once without adding iteration.
        for x in str(self.appSettings.allKeys().join(";")).split(";"): #Why join and resplit?
            if groupName in x:
                #We are sure the group exists so we can continue
                return True

    def resetSettings(self):
        self.appSettings.clear()

    def loadSettings(self, optionsMenu=False, data={}):
        global _ALWAYS_ON_TOP_
        #data is a dictionary where the key is the subgroup and the value is a list containing the key(s) we are looking for
        # Example: passing this:  data["LastAppState"] = ["windowPos"]
        #          would return the saved window position
        #If you want more than one key from a subgroup then just include it in the list
        # Example: passing this:  data["LastAppState"] = ["windowSize", "windowsPos"]
        #          would return both the saved size and the position.

        #Options menu is asking for the user's saved settings
        if optionsMenu is True:
            self.appSettings.beginGroup("Options")
            returnData = {}
            #loop through data{} and get the values requested. Each key is the subgroup name.
            for key in data:
                returnData[key] = []
                self.appSettings.beginGroup(key)
                #loop through the list of values to return and get the data
                for value in data[key]:
                    niceVal = str(self.appSettings.value(value).toPyObject())
                    returnData[key].append(niceVal)
                self.appSettings.endGroup()

            self.appSettings.endGroup()

            #We should have a nice dictionary with all the requested data in it so just return
            return returnData

        #We have a ton of settings to load and set so lets start with the basics
        #Load up the window size and position if they exist
        if self.testSettingGroup("WindowState") is True:
            self.appSettings.beginGroup("WindowState")
            self.UI.MainWindow.resize(self.appSettings.value("windowSize").toSize())
            self.UI.MainWindow.move(self.appSettings.value("windowPos").toPoint())
            self.appSettings.endGroup()
        #Now we load up our options if they exist, if not we create it and set the defaults.
        if self.testSettingGroup("Options") is True:
            #Load up the settings using the options window's loadOptions function
            loadedOptions = self.optionsWindowui.loadOptions(external=True, MW=self)
        else:
            loadedOptions = {'Appearance': ['MS Shell Dlg 2, 8', '#FFFFFF', '#000000'], 'fb2kServerInfo': ['127.0.0.1', '8888', False, '', ''], 'Advanced': [False, False, '', '0.65', True]}

        self.setupUiOptions(loadedOptions)
        _ALWAYS_ON_TOP_ = loadedOptions["Advanced"][4]



    def setupUiOptions(self, options):
        #Set the templates installed
        self.address = (options["fb2kServerInfo"][0], options["fb2kServerInfo"][1])
        self.webStatus_URL = "http://"
        #Set up the options we've been given

        #First we set the status page url with the given info.
        #Credentials
        if options["fb2kServerInfo"][2] is True: self.webStatus_URL += "%s:%s@" % (options["fb2kServerInfo"][3], options["fb2kServerInfo"][4])
        #IP and port
        self.webStatus_URL += "%s:%s/ajquery/index.html" % (options["fb2kServerInfo"][0], options["fb2kServerInfo"][1])

        #Set the URL
        self.UI.MainStatusWebView.setUrl(QtCore.QUrl(_fromUtf8(self.webStatus_URL)))

        #Now we set the user-defined appearance settings.
        self.fontStyle = options["Appearance"][0]
        self.fontBgColor = options["Appearance"][1]
        self.fontFgColor = options["Appearance"][2]

        #Now on to the advanced page
        lwop = {}
        #Set the debug mode/write mode
        lwop["debugModeEnabled"] = options["Advanced"][0]
        lwop["debugWriteEnabled"] = options["Advanced"][1]
        lwop["debugOutputFolder"] = options["Advanced"][2]
        lwop["masterMatchRatio"] = options["Advanced"][3]
        self.lyricsProg.setInternalOptions(lwop)

    def clear_console(self):
        self.output = []
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
            text = timestamp + text
            self.output.append(text)
            final_output = ""
            for entry in self.output:
                final_output = final_output + str(entry) + "<br>"


            html = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
</style></head><body style=" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">%s</p></body></html>
''' % final_output
            self.UI.consoleOutput.setHtml(_translate("MainWindow", html, None))

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

    def clearLyricsCacheAction(self):
        #U sure?
        if QtGui.QMessageBox.question(self.UI.MainWindow, "Clear Lyrics Cache?", "<p align='center'>Are you sure you want to remove all cached lyrics?<br>(This cannot be undone)</p>", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes:
            numfiles = self.lyricsProg.songCache.clearLyricsCache()
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
        self.lyricsProg.songCache.saveLyrics(self.lyricsProg.song, self.lyricsProg.artist, newlyrics.encode("utf8"))
        self.resetEditLyricsState()
        self.refreshLyricsButtonAction()

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
