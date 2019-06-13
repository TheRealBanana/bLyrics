from PyQt4 import QtCore, QtGui
from os import getcwd
import win32gui, win32con
from re import split as REsplit
from functools import partial
from ..fake_cell_widget import Ui_fakeCellWidget

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



class optionsDialogFunctions(object):
    def __init__(self, widget, uiFunctionsReference):
        self.uiFunctionsReference = uiFunctionsReference
        self.OptionsDialog = uiFunctionsReference.optionsWindowui
        self.settings = uiFunctionsReference.loadedOptions
        self.AOT = self.settings["Advanced"]["alwaysOnTop"]
        self.widget = widget
        self.curDir = getcwd()
        self.setDir = self.curDir
        #Set up connections and then apply our settings to our UI elements
        self.setupConnections()
        self.applyOptionsToUi()

    def setupConnections(self):
        self.OptionsDialog.optionsTabContainer.setCurrentIndex(0)
        QtCore.QObject.connect(self.OptionsDialog.debugEnabledCheck, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.OptionsDialog.debugWriteCheck.setEnabled)
        QtCore.QObject.connect(self.OptionsDialog.debugEnabledCheck, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.OptionsDialog.browseButton.setEnabled)
        QtCore.QObject.connect(self.OptionsDialog.debugEnabledCheck, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.OptionsDialog.folderPathText.setEnabled)
        QtCore.QObject.connect(self.OptionsDialog.debugEnabledCheck, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.uncheckDbgWrite)
        QtCore.QObject.connect(self.OptionsDialog.saveCancelButtons, QtCore.SIGNAL(_fromUtf8("rejected()")), self.widget.reject)
        QtCore.QObject.connect(self.OptionsDialog.saveCancelButtons, QtCore.SIGNAL(_fromUtf8("accepted()")), self.saveOptions)
        QtCore.QObject.connect(self.OptionsDialog.saveCancelButtons, QtCore.SIGNAL(_fromUtf8("clicked(QAbstractButton*)")), self.widget.update)
        QtCore.QObject.connect(self.OptionsDialog.reqCredsCheck, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.OptionsDialog.credentialsGroup.setEnabled)
        QtCore.QObject.connect(self.OptionsDialog.browseButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.popupLogSavePath)
        QtCore.QObject.connect(self.OptionsDialog.resetButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.resetUi)
        QtCore.QObject.connect(self.OptionsDialog.selectFontButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.selectFont)
        QtCore.QObject.connect(self.OptionsDialog.fgColorSelector, QtCore.SIGNAL(_fromUtf8("clicked()")), self.selectFgColor)
        QtCore.QObject.connect(self.OptionsDialog.bgColorSelector, QtCore.SIGNAL(_fromUtf8("clicked()")), self.selectBgColor)
        QtCore.QMetaObject.connectSlotsByName(self.widget)

        self.OptionsDialog = self.OptionsDialog
    def uncheckDbgWrite(self, _):
        if self.OptionsDialog.debugWriteCheck.isChecked():
            self.OptionsDialog.debugWriteCheck.setChecked(0)

    #Would be nice to consolidate the default options used here and in UIFunctions.loadSettings so that
    #we only need to change them in one spot if we need to at all.
    def resetUi(self):
        #We just reset the UI to the default settings, nothing complex.
        #Page One
        self.OptionsDialog.fontSelectionTextbox.setText(_translate("OptionsDialog", "Tahoma, 8", None))
        self.fontSelection = "Tahoma, 8"
        self.OptionsDialog.bgColorSelector.currentColor = "#FFFFFF"
        self.OptionsDialog.fgColorSelector.currentColor = "#000000"
        self.OptionsDialog.bgColorSelector.setStyleSheet(_fromUtf8("background-color: %s;" % self.OptionsDialog.bgColorSelector.currentColor))
        self.OptionsDialog.fgColorSelector.setStyleSheet(_fromUtf8("background-color: %s;" % self.OptionsDialog.fgColorSelector.currentColor))
        self.OptionsDialog.fontPreviewBox.setStyleSheet(_fromUtf8("color: rgb(0, 0, 0); font: 8pt \"Tahoma\"; background-color: rgb(255, 255, 255);"))


        #Page Two
        self.OptionsDialog.addressInput.setText(_translate("OptionsDialog", "127.0.0.1", None))
        self.OptionsDialog.portTextInput.setText(_translate("OptionsDialog", "8888", None))
        self.OptionsDialog.reqCredsCheck.setChecked(0)
        self.OptionsDialog.credentialsGroup.setEnabled(False)
        self.OptionsDialog.passwordTextInput.setText("")
        self.OptionsDialog.usernameTextInput.setText("")


        #Page Three
        self.OptionsDialog.debugEnabledCheck.setChecked(0)
        self.OptionsDialog.debugWriteCheck.setChecked(0)
        self.OptionsDialog.debugWriteCheck.setEnabled(False)
        self.OptionsDialog.browseButton.setEnabled(False)
        self.OptionsDialog.folderPathText.setEnabled(False)
        self.OptionsDialog.folderPathText.setText(self.curDir)
        self.setDir = self.curDir
        self.OptionsDialog.MRSelector.setProperty("value", 0.65)
        self.OptionsDialog.alwaysOnTopCheck.setChecked(0)
        #TODO ADD RESET FOR ROWS IN QLISTWIDGET


    def saveOptions(self):
        #Using the same data structure that loadSettings and saveSettings will be using
        #Theres something to be said about rigid data structures in typed languages.
        #Will have to look into maybe a namedtuple thingy if I ever get bored enough. :)

        data = {}

        #Page One - Appearance
        data["Appearance"] = {}
        data["Appearance"]["fontNameAndSize"] = str(self.OptionsDialog.fontSelectionTextbox.text())
        data["Appearance"]["bgFontColor"] = str(self.OptionsDialog.bgColorSelector.currentColor)
        data["Appearance"]["fgFontColor"] = str(self.OptionsDialog.fgColorSelector.currentColor)

        #Page Two - fb2kServerInfo
        data["fb2kServerInfo"] = {}
        data["fb2kServerInfo"]["address"] = str(self.OptionsDialog.addressInput.text())
        data["fb2kServerInfo"]["port"] = str(self.OptionsDialog.portTextInput.text())
        data["fb2kServerInfo"]["userpassreq"] = self.OptionsDialog.reqCredsCheck.isChecked()
        data["fb2kServerInfo"]["user"] = str(self.OptionsDialog.usernameTextInput.text())
        data["fb2kServerInfo"]["pass"] = str(self.OptionsDialog.passwordTextInput.text())

        #Page Three - Advanced
        data["Advanced"] = {}
        data["Advanced"]["debugModeEnabled"] = self.OptionsDialog.debugEnabledCheck.isChecked()
        data["Advanced"]["debugWriteEnabled"] = self.OptionsDialog.debugWriteCheck.isChecked()
        data["Advanced"]["debugOutputFolder"] = str(self.OptionsDialog.folderPathText.text())
        data["Advanced"]["masterMatchRatio"] = str(self.OptionsDialog.MRSelector.value())
        data["Advanced"]["alwaysOnTop"] = self.OptionsDialog.alwaysOnTopCheck.isChecked()

        data["lyricsSource"]["lyricsSourceList"] = self.getLyricsSourceList()

        self.uiFunctionsReference.saveSettings(data)
        self.uiFunctionsReference.appSettings.sync()
        self.widget.accept()

    def getLyricsSourceList(self):
        pass
        #Will just store the proper data in the UserData role for the row

    def applyOptionsToUi(self):
        #And now we set up the options UI with the correct options

        #Page One - Appearance
        self.fontSelection = self.settings["Appearance"]["fontNameAndSize"]
        fontFamily, size = REsplit(",", self.fontSelection)
        fontFamily = fontFamily.strip()
        fontSize = size.strip()
        self.OptionsDialog.fontSelectionTextbox.setText(_translate("OptionsDialog", self.fontSelection, None))
        self.OptionsDialog.bgColorSelector.currentColor = self.settings["Appearance"]["bgFontColor"]
        self.OptionsDialog.fgColorSelector.currentColor = self.settings["Appearance"]["fgFontColor"]
        self.OptionsDialog.bgColorSelector.setStyleSheet(_fromUtf8("background-color: %s;" % (self.settings["Appearance"]["bgFontColor"])))
        self.OptionsDialog.fgColorSelector.setStyleSheet(_fromUtf8("background-color: %s;" % (self.settings["Appearance"]["fgFontColor"])))
        self.OptionsDialog.fontPreviewBox.setStyleSheet(_fromUtf8("color: %s; font: %spt \"%s\"; background-color: %s;" % (self.settings["Appearance"]["fgFontColor"], fontSize, fontFamily, self.settings["Appearance"]["bgFontColor"])))

        #Page Two - fb2kServerInfo
        self.OptionsDialog.addressInput.setText(_translate("OptionsDialog", self.settings["fb2kServerInfo"]["address"], None))
        self.OptionsDialog.portTextInput.setText(_translate("OptionsDialog", self.settings["fb2kServerInfo"]["port"], None))
        self.OptionsDialog.reqCredsCheck.setChecked(self.settings["fb2kServerInfo"]["userpassreq"])
        self.OptionsDialog.credentialsGroup.setEnabled(self.settings["fb2kServerInfo"]["userpassreq"])
        self.OptionsDialog.usernameTextInput.setText(_translate("OptionsDialog", self.settings["fb2kServerInfo"]["user"], None))
        self.OptionsDialog.passwordTextInput.setText(_translate("OptionsDialog", self.settings["fb2kServerInfo"]["pass"], None))

        #Page Three - Advanced
        self.OptionsDialog.debugEnabledCheck.setChecked(self.settings["Advanced"]["debugModeEnabled"])
        self.OptionsDialog.debugWriteCheck.setEnabled(self.settings["Advanced"]["debugModeEnabled"])
        self.OptionsDialog.browseButton.setEnabled(self.settings["Advanced"]["debugModeEnabled"])
        self.OptionsDialog.folderPathText.setEnabled(self.settings["Advanced"]["debugModeEnabled"])
        self.OptionsDialog.debugWriteCheck.setChecked(self.settings["Advanced"]["debugWriteEnabled"])
        self.OptionsDialog.folderPathText.setText(_translate("OptionsDialog", self.settings["Advanced"]["debugOutputFolder"], None))
        self.setDir = self.settings["Advanced"]["debugOutputFolder"]
        self.OptionsDialog.MRSelector.setValue(float(self.settings["Advanced"]["masterMatchRatio"]))
        self.OptionsDialog.alwaysOnTopCheck.setChecked(self.settings["Advanced"]["alwaysOnTop"])

        #Page Four - Lyrics Sources
        # Data format:
        # dict[filename] = [propername, version, enableddisabled]
        for source in self.settings["lyricsSource"]:
            rowItem = QtGui.QListWidgetItem(self.OptionsDialog.lyricsSourceWidget)
            #rowData[0] = Lyrics provider name
            #rowData[1] = provider version
            #rowData[2] = file name (make sure to add tool hint with full path)
            #rowData[3] = list index (based on priority, maybe just straight priority)
            rowData = [source.LYRICS_PROVIDER_NAME, source.LYRICS_PROVIDER_VERSION, source.__file__, str(source.LYRICS_PROVIDER_PRIORITY)]
            rowWidget = Ui_fakeCellWidget(rowData=rowData)
            if self.OptionsDialog.lyricsSourceWidget.count() % 2 == 0: #Alternate row background
                rowWidget.setStyleSheet("background-color: rgb(209, 220, 255);")
            else:
                rowWidget.setStyleSheet("background-color: rgb(188, 205, 255);")
            self.OptionsDialog.lyricsSourceWidget.addItem(rowItem)
            self.OptionsDialog.lyricsSourceWidget.setItemWidget(rowItem, rowWidget)

            #filename, [propername, version, enableddisabled] in self.settings["lyricsSource"]["lyricsSourceList"]:
            #self.OptionsDialog.lyricsSourceWidget.addItem(source.LYRICS_PROVIDER_NAME)

    def selectFont(self):
        fontDialog = QtGui.QFontDialog()
        fontFamily, size = REsplit(",", self.fontSelection)
        fontFamily = fontFamily.strip()
        fontSize = int(size.strip())
        self.timer = QtCore.QTimer()
        aotFunc = partial(self.forceDialogOnTop, "Select Font")
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), aotFunc)
        self.timer.start(25)
        retFont = fontDialog.getFont(QtGui.QFont(fontFamily, fontSize))
        fontFamily = retFont[0].family()
        fontSize = retFont[0].pointSize()
        self.fontSelection = str(fontFamily) + ", " + str(fontSize)
        self.updatePreviewBoxCSS()
        self.OptionsDialog.fontSelectionTextbox.setText(_translate("OptionsDialog", self.fontSelection, None))


    def updatePreviewBoxCSS(self):
        fontFamily, size = REsplit(",", self.fontSelection)
        fontFamily = fontFamily.strip()
        fontSize = size.strip()
        self.OptionsDialog.fontPreviewBox.setStyleSheet(_fromUtf8("color: %s; font: %spt \"%s\"; background-color: %s;" % (self.OptionsDialog.fgColorSelector.currentColor, fontSize, fontFamily, self.OptionsDialog.bgColorSelector.currentColor)))

    def colorPopup(self, startColor="#FFFFFF"):
        #Create the color dialog object
        color = QtGui.QColorDialog()
        #create the QTimer and connect its timeout() signal to a function that sets the color dialog to be topmost
        #We have to do it this way because normally the QColorDialog halts the current thread.
        #The only way to set the window top-most is to set it this way from a different thread.
        #QTimer facilitates this on a basic level without needing to fuss with complex QThreads.
        self.timer = QtCore.QTimer()
        aotFunc = partial(self.forceDialogOnTop, "Select Color")
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), aotFunc)
        self.timer.start(25)
        #Create a QColor object for the startColor
        propColor = QtGui.QColor()
        propColor.setNamedColor(str(startColor))
        #Now we open the color dialog and get the color, returning it as selectedColor which is a QColor object.
        selectedColor = color.getColor(propColor)
        if selectedColor.isValid():
            return selectedColor.name()
        else:
            return startColor


    def selectBgColor(self):
        bgColor = self.colorPopup(self.OptionsDialog.bgColorSelector.currentColor)
        self.OptionsDialog.bgColorSelector.currentColor = bgColor
        self.OptionsDialog.bgColorSelector.setStyleSheet(_fromUtf8("background-color: %s;" % bgColor))
        self.updatePreviewBoxCSS()

    def selectFgColor(self):
        fgColor = self.colorPopup(self.OptionsDialog.fgColorSelector.currentColor)
        self.OptionsDialog.fgColorSelector.currentColor = fgColor
        self.OptionsDialog.fgColorSelector.setStyleSheet(_fromUtf8("background-color: %s;" % fgColor))
        self.updatePreviewBoxCSS()

    #Some dialogs can't be forced to be on top using window hints like other dialogs so we improvise
    def forceDialogOnTop(self, dialogTitle):
        #Kind of a nasty hack here. The QColorDialog seems to be impossible to open on top of all other windows.
        #So we have to manually set the window position using win32gui and win32con
        if self.AOT is True:
            cpHandle = win32gui.FindWindow(None, dialogTitle)
            cpPos = win32gui.GetWindowRect(cpHandle)
            win32gui.SetWindowPos(cpHandle, win32con.HWND_TOPMOST, cpPos[0], cpPos[1], int(cpPos[2]-cpPos[0]), int(cpPos[3]-cpPos[1]), 0)
        #Kill the timer
        self.timer.stop()

    def popupLogSavePath(self):
        fileDialog = QtGui.QFileDialog()
        #fileDialog.AcceptMode = 1
        fileDialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        chosenFile = fileDialog.getExistingDirectory(caption="Choose where to save debug output...", directory=self.setDir)
        self.OptionsDialog.folderPathText.setText(_translate("OptionsDialog", chosenFile, None))