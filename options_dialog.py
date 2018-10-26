# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'options_dialog.ui'
#
# Created: Thu Sep 18 21:25:10 2014
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!





# tab_General -> tab_Appearance
# themeSelectionGroup -> fontSelectionGroup
# otherOptionsGroup -> colorSelectionGroup




from PyQt4 import QtCore, QtGui
from os import getcwd
import win32gui, win32con
from re import split as REsplit
_CURDIR = getcwd()
_SETDIR = _CURDIR

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

class Ui_OptionsDialog(object):
    def setupUi(self, OptionsDialog, MainWindow, aot):
        self.MainWindow = MainWindow
        self.opACCEPT = OptionsDialog.accept
        self.AOT = aot

        OptionsDialog.setObjectName(_fromUtf8("OptionsDialog"))
        OptionsDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        OptionsDialog.resize(350, 330)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(OptionsDialog.sizePolicy().hasHeightForWidth())
        OptionsDialog.setSizePolicy(sizePolicy)
        OptionsDialog.setMinimumSize(QtCore.QSize(350, 330))
        OptionsDialog.setMaximumSize(QtCore.QSize(350, 330))
        OptionsDialog.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        OptionsDialog.setLayoutDirection(QtCore.Qt.LeftToRight)
        OptionsDialog.setAutoFillBackground(False)
        OptionsDialog.setModal(True)

        #Tab One, Appearance
        self.optionsTabContainer = QtGui.QTabWidget(OptionsDialog)
        self.optionsTabContainer.setGeometry(QtCore.QRect(9, 9, 331, 285))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.optionsTabContainer.sizePolicy().hasHeightForWidth())
        self.optionsTabContainer.setSizePolicy(sizePolicy)
        self.optionsTabContainer.setMinimumSize(QtCore.QSize(331, 285))
        self.optionsTabContainer.setMaximumSize(QtCore.QSize(331, 285))
        self.optionsTabContainer.setTabsClosable(False)
        self.optionsTabContainer.setObjectName(_fromUtf8("optionsTabContainer"))
        self.tab_Appearance = QtGui.QWidget()
        self.tab_Appearance.setObjectName(_fromUtf8("tab_Appearance"))
        self.fontSelectionGroup = QtGui.QGroupBox(self.tab_Appearance)
        self.fontSelectionGroup.setGeometry(QtCore.QRect(10, 10, 307, 76))
        self.fontSelectionGroup.setObjectName(_fromUtf8("fontSelectionGroup"))
        self.selectFontButton = QtGui.QPushButton(self.fontSelectionGroup)
        self.selectFontButton.setGeometry(QtCore.QRect(220, 30, 75, 23))
        self.selectFontButton.setDefault(False)
        self.selectFontButton.setObjectName(_fromUtf8("selectFontButton"))
        self.fontSelectionTextbox = QtGui.QLineEdit(self.fontSelectionGroup)
        self.fontSelectionTextbox.setEnabled(True)
        self.fontSelectionTextbox.setGeometry(QtCore.QRect(10, 32, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fontSelectionTextbox.setFont(font)
        self.fontSelectionTextbox.setReadOnly(True)
        self.fontSelectionTextbox.setObjectName(_fromUtf8("fontSelectionTextbox"))
        self.colorSelectionGroup = QtGui.QGroupBox(self.tab_Appearance)
        self.colorSelectionGroup.setGeometry(QtCore.QRect(9, 91, 307, 91))
        self.colorSelectionGroup.setAutoFillBackground(False)
        self.colorSelectionGroup.setFlat(False)
        self.colorSelectionGroup.setObjectName(_fromUtf8("colorSelectionGroup"))
        self.bgColorLabel = QtGui.QLabel(self.colorSelectionGroup)
        self.bgColorLabel.setGeometry(QtCore.QRect(20, 54, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.bgColorLabel.setFont(font)
        self.bgColorLabel.setObjectName(_fromUtf8("bgColorLabel"))
        self.fgColorLabel = QtGui.QLabel(self.colorSelectionGroup)
        self.fgColorLabel.setGeometry(QtCore.QRect(21, 18, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.fgColorLabel.setFont(font)
        self.fgColorLabel.setObjectName(_fromUtf8("fgColorLabel"))
        self.fgColorSelectorFrame = QtGui.QFrame(self.colorSelectionGroup)
        self.fgColorSelectorFrame.setGeometry(QtCore.QRect(116, 16, 24, 24))
        self.fgColorSelectorFrame.setFrameShape(QtGui.QFrame.WinPanel)
        self.fgColorSelectorFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.fgColorSelectorFrame.setLineWidth(3)
        self.fgColorSelectorFrame.setMidLineWidth(2)
        self.fgColorSelectorFrame.setObjectName(_fromUtf8("fgColorSelectorFrame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.fgColorSelectorFrame)
        self.horizontalLayout.setMargin(1)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.fgColorSelector = QtGui.QToolButton(self.fgColorSelectorFrame)
        self.fgColorSelector.setAutoFillBackground(False)
        self.fgColorSelector.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 0);"))
        self.fgColorSelector.setText(_fromUtf8(""))
        self.fgColorSelector.setIconSize(QtCore.QSize(16, 16))
        self.fgColorSelector.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.fgColorSelector.setAutoRaise(True)
        self.fgColorSelector.setObjectName(_fromUtf8("fgColorSelector"))
        self.horizontalLayout.addWidget(self.fgColorSelector)
        self.bgColorSelectorFrame = QtGui.QFrame(self.colorSelectionGroup)
        self.bgColorSelectorFrame.setGeometry(QtCore.QRect(116, 52, 24, 24))
        self.bgColorSelectorFrame.setFrameShape(QtGui.QFrame.WinPanel)
        self.bgColorSelectorFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.bgColorSelectorFrame.setLineWidth(3)
        self.bgColorSelectorFrame.setMidLineWidth(2)
        self.bgColorSelectorFrame.setObjectName(_fromUtf8("bgColorSelectorFrame"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.bgColorSelectorFrame)
        self.horizontalLayout_2.setMargin(1)
        self.horizontalLayout_2.setSpacing(1)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.bgColorSelector = QtGui.QToolButton(self.bgColorSelectorFrame)
        self.bgColorSelector.setAutoFillBackground(False)
        self.bgColorSelector.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.bgColorSelector.setText(_fromUtf8(""))
        self.bgColorSelector.setIconSize(QtCore.QSize(16, 16))
        self.bgColorSelector.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.bgColorSelector.setAutoRaise(True)
        self.bgColorSelector.setObjectName(_fromUtf8("bgColorSelector"))
        self.horizontalLayout_2.addWidget(self.bgColorSelector)
        self.fontPreviewLabel = QtGui.QLabel(self.tab_Appearance)
        self.fontPreviewLabel.setGeometry(QtCore.QRect(10, 182, 71, 20))
        self.fontPreviewLabel.setObjectName(_fromUtf8("fontPreviewLabel"))
        self.fontPreviewBox = QtGui.QPlainTextEdit(self.tab_Appearance)
        self.fontPreviewBox.setGeometry(QtCore.QRect(13, 200, 301, 51))
        self.fontPreviewBox.setStyleSheet(_fromUtf8("color: rgb(0, 0, 0);\n"
                                                    "font: 8pt \"MS Shell Dlg 2\";\n"
                                                    "background-color: rgb(255, 255, 255);"))
        self.fontPreviewBox.setObjectName(_fromUtf8("fontPreviewBox"))
        self.optionsTabContainer.addTab(self.tab_Appearance, _fromUtf8(""))
        ## END TAB ONE - APPEARANCE ##






        # TAB TWO - FOOBAR2K SERVER INFO
        self.tab_WebInterface = QtGui.QWidget()
        self.tab_WebInterface.setObjectName(_fromUtf8("tab_WebInterface"))
        self.tab_WebInterface_GridLayout = QtGui.QGridLayout(self.tab_WebInterface)
        self.tab_WebInterface_GridLayout.setObjectName(_fromUtf8("tab_WebInterface_GridLayout"))
        self.credentialsGroup = QtGui.QGroupBox(self.tab_WebInterface)
        self.credentialsGroup.setEnabled(False)
        self.credentialsGroup.setObjectName(_fromUtf8("credentialsGroup"))
        self.credentialsGroup_GridLayout = QtGui.QGridLayout(self.credentialsGroup)
        self.credentialsGroup_GridLayout.setObjectName(_fromUtf8("credentialsGroup_GridLayout"))
        self.usernameLabel = QtGui.QLabel(self.credentialsGroup)
        self.usernameLabel.setObjectName(_fromUtf8("usernameLabel"))
        self.credentialsGroup_GridLayout.addWidget(self.usernameLabel, 0, 0, 1, 1)
        self.passwordTextInput = QtGui.QLineEdit(self.credentialsGroup)
        self.passwordTextInput.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordTextInput.setObjectName(_fromUtf8("passwordTextInput"))
        self.credentialsGroup_GridLayout.addWidget(self.passwordTextInput, 1, 1, 1, 1)
        self.usernameTextInput = QtGui.QLineEdit(self.credentialsGroup)
        self.usernameTextInput.setObjectName(_fromUtf8("usernameTextInput"))
        self.credentialsGroup_GridLayout.addWidget(self.usernameTextInput, 0, 1, 1, 1)
        self.passwordLabel = QtGui.QLabel(self.credentialsGroup)
        self.passwordLabel.setObjectName(_fromUtf8("passwordLabel"))
        self.credentialsGroup_GridLayout.addWidget(self.passwordLabel, 1, 0, 1, 1)
        self.tab_WebInterface_GridLayout.addWidget(self.credentialsGroup, 1, 0, 1, 1)
        self.addressPortGroup = QtGui.QGroupBox(self.tab_WebInterface)
        self.addressPortGroup.setObjectName(_fromUtf8("addressPortGroup"))
        self.gridLayout = QtGui.QGridLayout(self.addressPortGroup)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.addressInput = QtGui.QLineEdit(self.addressPortGroup)
        self.addressInput.setInputMethodHints(QtCore.Qt.ImhUrlCharactersOnly)
        self.addressInput.setObjectName(_fromUtf8("addressInput"))
        self.gridLayout.addWidget(self.addressInput, 0, 0, 1, 1)
        self.colonLabel = QtGui.QLabel(self.addressPortGroup)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.colonLabel.setFont(font)
        self.colonLabel.setObjectName(_fromUtf8("colonLabel"))
        self.gridLayout.addWidget(self.colonLabel, 0, 1, 1, 1)
        self.portTextInput = QtGui.QLineEdit(self.addressPortGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.portTextInput.sizePolicy().hasHeightForWidth())
        self.portTextInput.setSizePolicy(sizePolicy)
        self.portTextInput.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.portTextInput.setInputMask(_fromUtf8(""))
        self.portTextInput.setMaxLength(32767)
        self.portTextInput.setFrame(True)
        self.portTextInput.setCursorPosition(4)
        self.portTextInput.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.portTextInput.setDragEnabled(True)
        self.portTextInput.setPlaceholderText(_fromUtf8(""))
        self.portTextInput.setObjectName(_fromUtf8("portTextInput"))
        self.gridLayout.addWidget(self.portTextInput, 0, 2, 1, 1)
        self.reqCredsCheck = QtGui.QCheckBox(self.addressPortGroup)
        self.reqCredsCheck.setObjectName(_fromUtf8("reqCredsCheck"))
        self.gridLayout.addWidget(self.reqCredsCheck, 1, 0, 1, 1)
        self.tab_WebInterface_GridLayout.addWidget(self.addressPortGroup, 0, 0, 1, 1)
        ## END TAB TWO - FOOBAR2K SERVER INFO



        # TAB THREE - ADVANCED
        self.optionsTabContainer.addTab(self.tab_WebInterface, _fromUtf8(""))
        self.tab_Advanced = QtGui.QWidget()
        self.tab_Advanced.setObjectName(_fromUtf8("tab_Advanced"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tab_Advanced)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.debugGroup = QtGui.QGroupBox(self.tab_Advanced)
        self.debugGroup.setObjectName(_fromUtf8("debugGroup"))
        self.debugGroup_GridLayout = QtGui.QGridLayout(self.debugGroup)
        self.debugGroup_GridLayout.setObjectName(_fromUtf8("debugGroup_GridLayout"))
        self.debugWriteCheck = QtGui.QCheckBox(self.debugGroup)
        self.debugWriteCheck.setEnabled(False)
        self.debugWriteCheck.setCheckable(True)
        self.debugWriteCheck.setTristate(False)
        self.debugWriteCheck.setObjectName(_fromUtf8("debugWriteCheck"))
        self.debugGroup_GridLayout.addWidget(self.debugWriteCheck, 1, 0, 1, 1)
        self.debugEnabledCheck = QtGui.QCheckBox(self.debugGroup)
        self.debugEnabledCheck.setObjectName(_fromUtf8("debugEnabledCheck"))
        self.debugGroup_GridLayout.addWidget(self.debugEnabledCheck, 0, 0, 1, 1)
        self.selectFolderGroup = QtGui.QGroupBox(self.debugGroup)
        self.selectFolderGroup.setObjectName(_fromUtf8("selectFolderGroup"))
        self.selectFolderGroup_GridLayout = QtGui.QGridLayout(self.selectFolderGroup)
        self.selectFolderGroup_GridLayout.setObjectName(_fromUtf8("selectFolderGroup_GridLayout"))
        self.folderPathText = QtGui.QLineEdit(self.selectFolderGroup)
        self.folderPathText.setEnabled(True)
        self.folderPathText.setEchoMode(QtGui.QLineEdit.Normal)
        self.folderPathText.setDragEnabled(True)
        self.folderPathText.setReadOnly(True)
        self.folderPathText.setObjectName(_fromUtf8("folderPathText"))
        self.selectFolderGroup_GridLayout.addWidget(self.folderPathText, 0, 0, 1, 1)
        self.browseButton = QtGui.QPushButton(self.selectFolderGroup)
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.selectFolderGroup_GridLayout.addWidget(self.browseButton, 0, 1, 1, 1)
        self.debugGroup_GridLayout.addWidget(self.selectFolderGroup, 3, 0, 1, 1)
        self.verticalLayout.addWidget(self.debugGroup)
        self.internalStuffGroup = QtGui.QGroupBox(self.tab_Advanced)
        self.internalStuffGroup.setObjectName(_fromUtf8("internalStuffGroup"))
        self.formLayout = QtGui.QFormLayout(self.internalStuffGroup)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.MRLabel = QtGui.QLabel(self.internalStuffGroup)
        self.MRLabel.setObjectName(_fromUtf8("MRLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.MRLabel)
        self.MRSelector = QtGui.QDoubleSpinBox(self.internalStuffGroup)
        self.MRSelector.setDecimals(2)
        self.MRSelector.setMinimum(0.01)
        self.MRSelector.setMaximum(0.99)
        self.MRSelector.setSingleStep(0.01)
        self.MRSelector.setProperty("value", 0.65)
        self.MRSelector.setObjectName(_fromUtf8("MRSelector"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.MRSelector)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.setItem(1, QtGui.QFormLayout.FieldRole, spacerItem)
        self.alwaysOnTopCheck = QtGui.QCheckBox(self.internalStuffGroup)
        self.alwaysOnTopCheck.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.alwaysOnTopCheck.setObjectName(_fromUtf8("alwaysOnTopCheck"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.alwaysOnTopCheck)
        self.verticalLayout.addWidget(self.internalStuffGroup)
        self.optionsTabContainer.addTab(self.tab_Advanced, _fromUtf8(""))
        ## END TAB THREE - ADVANCED


        self.buttonFrame = QtGui.QFrame(OptionsDialog)
        self.buttonFrame.setGeometry(QtCore.QRect(10, 300, 331, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonFrame.sizePolicy().hasHeightForWidth())
        self.buttonFrame.setSizePolicy(sizePolicy)
        self.buttonFrame.setFrameShape(QtGui.QFrame.NoFrame)
        self.buttonFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.buttonFrame.setLineWidth(0)
        self.buttonFrame.setObjectName(_fromUtf8("buttonFrame"))
        self.saveCancelButtons = QtGui.QDialogButtonBox(self.buttonFrame)
        self.saveCancelButtons.setGeometry(QtCore.QRect(79, 0, 151, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveCancelButtons.sizePolicy().hasHeightForWidth())
        self.saveCancelButtons.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.saveCancelButtons.setFont(font)
        self.saveCancelButtons.setOrientation(QtCore.Qt.Horizontal)
        self.saveCancelButtons.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.saveCancelButtons.setCenterButtons(True)
        self.saveCancelButtons.setObjectName(_fromUtf8("saveCancelButtons"))
        self.resetButton = QtGui.QPushButton(self.buttonFrame)
        self.resetButton.setGeometry(QtCore.QRect(0, 0, 73, 23))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        self.resetButton.setFont(font)
        self.resetButton.setObjectName(_fromUtf8("resetButton"))
        self.bgColorLabel.setBuddy(self.bgColorSelector)
        self.fgColorLabel.setBuddy(self.fgColorSelector)
        self.fontPreviewLabel.setBuddy(self.fontPreviewBox)
        self.usernameLabel.setBuddy(self.usernameTextInput)
        self.passwordLabel.setBuddy(self.passwordTextInput)
        self.MRLabel.setBuddy(self.MRSelector)

        self.retranslateUi(OptionsDialog)
        self.optionsTabContainer.setCurrentIndex(0)

        OptionsDialog.setTabOrder(self.optionsTabContainer, self.selectFontButton)
        OptionsDialog.setTabOrder(self.selectFontButton, self.fontSelectionTextbox)
        OptionsDialog.setTabOrder(self.fontSelectionTextbox, self.fgColorSelector)
        OptionsDialog.setTabOrder(self.fgColorSelector, self.bgColorSelector)
        OptionsDialog.setTabOrder(self.bgColorSelector, self.fontPreviewBox)
        OptionsDialog.setTabOrder(self.fontPreviewBox, self.addressInput)
        OptionsDialog.setTabOrder(self.addressInput, self.portTextInput)
        OptionsDialog.setTabOrder(self.portTextInput, self.reqCredsCheck)
        OptionsDialog.setTabOrder(self.reqCredsCheck, self.usernameTextInput)
        OptionsDialog.setTabOrder(self.usernameTextInput, self.passwordTextInput)
        OptionsDialog.setTabOrder(self.passwordTextInput, self.debugEnabledCheck)
        OptionsDialog.setTabOrder(self.debugEnabledCheck, self.debugWriteCheck)
        OptionsDialog.setTabOrder(self.debugWriteCheck, self.browseButton)
        OptionsDialog.setTabOrder(self.browseButton, self.folderPathText)
        OptionsDialog.setTabOrder(self.folderPathText, self.MRSelector)
        OptionsDialog.setTabOrder(self.MRSelector, self.alwaysOnTopCheck)
        OptionsDialog.setTabOrder(self.alwaysOnTopCheck, self.resetButton)
        OptionsDialog.setTabOrder(self.resetButton, self.saveCancelButtons)

        #If we have options already saved, load them
        if self.MainWindow.testSettingGroup("Options") is True:
            self.loadOptions()

        self.optionsTabContainer.setCurrentIndex(0)
        QtCore.QObject.connect(self.debugEnabledCheck, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.debugWriteCheck.setEnabled)
        QtCore.QObject.connect(self.debugEnabledCheck, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.browseButton.setEnabled)
        QtCore.QObject.connect(self.debugEnabledCheck, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.folderPathText.setEnabled)
        QtCore.QObject.connect(self.debugEnabledCheck, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.uncheckDbgWrite)
        QtCore.QObject.connect(self.saveCancelButtons, QtCore.SIGNAL(_fromUtf8("rejected()")), OptionsDialog.reject)
        QtCore.QObject.connect(self.saveCancelButtons, QtCore.SIGNAL(_fromUtf8("accepted()")), self.saveOptions)
        QtCore.QObject.connect(self.saveCancelButtons, QtCore.SIGNAL(_fromUtf8("clicked(QAbstractButton*)")), OptionsDialog.update)
        QtCore.QObject.connect(self.reqCredsCheck, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.credentialsGroup.setEnabled)
        QtCore.QObject.connect(self.browseButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.popupLogSavePath)
        QtCore.QObject.connect(self.resetButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.resetUi)
        QtCore.QObject.connect(self.selectFontButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.selectFont)
        QtCore.QObject.connect(self.fgColorSelector, QtCore.SIGNAL(_fromUtf8("clicked()")), self.selectFgColor)
        QtCore.QObject.connect(self.bgColorSelector, QtCore.SIGNAL(_fromUtf8("clicked()")), self.selectBgColor)
        QtCore.QMetaObject.connectSlotsByName(OptionsDialog)

        self.OptionsDialog = OptionsDialog

    def uncheckDbgWrite(self, toggledstate):
        checkstate = self.debugWriteCheck.isChecked()
        if checkstate is True:
            self.debugWriteCheck.setChecked(0)

    def resetUi(self):
        global _SETDIR
        #We just reset the UI to the default settings, nothing complex.
        #Page One
        self.fontSelectionTextbox.setText(_translate("OptionsDialog", "Tahoma, 8", None))
        self.fontSelection = "Tahoma, 8"
        self.bgColorSelector.currentColor = "#FFFFFF"
        self.fgColorSelector.currentColor = "#000000"
        self.bgColorSelector.setStyleSheet(_fromUtf8("background-color: %s;" % (self.bgColorSelector.currentColor)))
        self.fgColorSelector.setStyleSheet(_fromUtf8("background-color: %s;" % (self.fgColorSelector.currentColor)))
        self.fontPreviewBox.setStyleSheet(_fromUtf8("color: rgb(0, 0, 0); font: 8pt \"Tahoma\"; background-color: rgb(255, 255, 255);"))


        #Page Two
        self.addressInput.setText(_translate("OptionsDialog", "127.0.0.1", None))
        self.portTextInput.setText(_translate("OptionsDialog", "8888", None))
        self.reqCredsCheck.setChecked(0)
        self.credentialsGroup.setEnabled(False)
        self.passwordTextInput.setText("")
        self.usernameTextInput.setText("")


        #Page Three
        self.debugEnabledCheck.setChecked(0)
        self.debugWriteCheck.setChecked(0)
        self.debugWriteCheck.setEnabled(False)
        self.browseButton.setEnabled(False)
        self.folderPathText.setEnabled(False)
        self.folderPathText.setText(_CURDIR)
        _SETDIR = _CURDIR
        self.MRSelector.setProperty("value", 0.65)
        self.alwaysOnTopCheck.setChecked(0)


    def saveOptions(self):
        #Ok we need to save everything from all three pages and pack that into a list of three dictionaries. Simple!
        #Just go over each page one by one, page one has nothing as of yet so its not here

        #Page One
        p1 = {}
        p1["fontNameAndSize"] = str(self.fontSelectionTextbox.text())
        p1["bgFontColor"] = str(self.bgColorSelector.currentColor)
        p1["fgFontColor"] = str(self.fgColorSelector.currentColor)

        #Page Two
        p2 = {}
        p2["address"] = str(self.addressInput.text())
        p2["port"] = str(self.portTextInput.text())
        p2["userpassreq"] = self.reqCredsCheck.isChecked()
        p2["user"] = str(self.usernameTextInput.text())
        p2["pass"] = str(self.passwordTextInput.text())

        #Page Three
        p3 = {}
        p3["debugModeEnabled"] = self.debugEnabledCheck.isChecked()
        p3["debugWriteEnabled"] = self.debugWriteCheck.isChecked()
        p3["debugOutputFolder"] = str(self.folderPathText.text())
        p3["masterMatchRatio"] = str(self.MRSelector.value())
        p3["alwaysOnTop"] = self.alwaysOnTopCheck.isChecked()

        data = [p1, p2, p3]

        self.MainWindow.saveSettings(optionsMenu=True, data=data)
        self.MainWindow.appSettings.sync()
        self.opACCEPT()


    def loadOptions(self, external=False, MW=None):
        global _SETDIR
        #Basically the same thing as saveOptions() except we have to set the widgets to their respective values instead of reading.
        #The loadSettings function of the parent window (MainWindow) requires setting load requests to be in the form of a dictionary of lists.
        # Each dictionary key is a subgroup and each value is a setting name. The return dictionary will be the same, each key is a subgroup
        # and each value is the value requested in the same order as requested (So keep track of that sort of thing!)
        requestedData = {}
        if MW is not None:
            MainWindow = MW
        else:
            MainWindow = self.MainWindow

        #Page One
        requestedData["Appearance"] = []
        requestedData["Appearance"].append("fontNameAndSize")
        requestedData["Appearance"].append("bgFontColor")
        requestedData["Appearance"].append("fgFontColor")

        #Page Two
        requestedData["fb2kServerInfo"] = []
        requestedData["fb2kServerInfo"].append("address")
        requestedData["fb2kServerInfo"].append("port")
        requestedData["fb2kServerInfo"].append("userpassreq")
        requestedData["fb2kServerInfo"].append("user")
        requestedData["fb2kServerInfo"].append("pass")
        requestedData["fb2kServerInfo"].append("installedTemplates")

        #Page Three
        requestedData["Advanced"] = []
        requestedData["Advanced"].append("debugModeEnabled")
        requestedData["Advanced"].append("debugWriteEnabled")
        requestedData["Advanced"].append("debugOutputFolder")
        requestedData["Advanced"].append("masterMatchRatio")
        requestedData["Advanced"].append("alwaysOnTop")

        #Gather the data
        #Ok so its possible that loadSettings will request this function, loadOptions, to return data, which requires us to call back to loadSettings.
        #Do you see how absurdly and needlessly complicated this is? Bad design. Most of this should be moved to loadSettings()
        returnData = MainWindow.loadSettings(optionsMenu=True, data=requestedData)

        #Some of the true/false option need to be corrected
        for key in returnData:
            for val in returnData[key]: # Could exchange this for enumerate to get the current index at the same time
                currentIndex = returnData[key].index(val)
                if isinstance(val, basestring):
                    if val == "true": returnData[key][currentIndex] = True
                    elif val == "false": returnData[key][currentIndex] = False
                if isinstance(val, list):
                    for x in val: #Same here, enumerate gets rid of the line below
                        cursubIndex = returnData[key][currentIndex].index(x)
                        if x == "true": returnData[key][currentIndex][cursubIndex] = True
                        elif x == "false": returnData[key][currentIndex][cursubIndex] = False


        #If this data was requested by something else we return the data
        if external == True:
            return returnData

        #And now we set up the options UI with the correct options

        #Page One
        p1 = returnData["Appearance"]
        self.fontSelection = p1[0]
        self.fontSelectionTextbox.setText(_translate("OptionsDialog", p1[0], None))
        self.bgColorSelector.currentColor = p1[1]
        self.fgColorSelector.currentColor = p1[2]
        self.bgColorSelector.setStyleSheet(_fromUtf8("background-color: %s;" % (p1[1])))
        self.fgColorSelector.setStyleSheet(_fromUtf8("background-color: %s;" % (p1[2])))
        fontFamily, size = REsplit(",", p1[0])
        fontFamily = fontFamily.strip()
        fontSize = size.strip()
        self.fontPreviewBox.setStyleSheet(_fromUtf8("color: %s; font: %spt \"%s\"; background-color: %s;" % (p1[2], fontSize, fontFamily, p1[1])))

        #Page Two
        p2 = returnData["fb2kServerInfo"]
        self.addressInput.setText(_translate("OptionsDialog", p2[0], None))
        self.portTextInput.setText(_translate("OptionsDialog", p2[1], None))
        self.reqCredsCheck.setChecked(p2[2])
        self.credentialsGroup.setEnabled(p2[2])
        self.usernameTextInput.setText(_translate("OptionsDialog", p2[3], None))
        self.passwordTextInput.setText(_translate("OptionsDialog", p2[4], None))

        #Page Three
        p3 = returnData["Advanced"]
        self.debugEnabledCheck.setChecked(p3[0])
        self.debugWriteCheck.setEnabled(p3[0])
        self.browseButton.setEnabled(p3[0])
        self.folderPathText.setEnabled(p3[0])
        self.debugWriteCheck.setChecked(p3[1])
        self.folderPathText.setText(_translate("OptionsDialog", p3[2], None))
        _SETDIR = p3[2]
        self.MRSelector.setValue(float(p3[3]))
        self.alwaysOnTopCheck.setChecked(p3[4])

    def selectFont(self):
        fontDialog = QtGui.QFontDialog()
        fontFamily, size = REsplit(",", self.fontSelection)
        fontFamily = fontFamily.strip()
        fontSize = int(size.strip())
        self.timer = QtCore.QTimer()
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.forceFontDialogOnTop)
        self.timer.start(25)
        retFont = fontDialog.getFont(QtGui.QFont(fontFamily, fontSize))
        fontFamily = retFont[0].family()
        fontSize = retFont[0].pointSize()
        self.fontSelection = str(fontFamily) + ", " + str(fontSize)
        self.updatePreviewBoxCSS()
        self.fontSelectionTextbox.setText(_translate("OptionsDialog", self.fontSelection, None))


    def updatePreviewBoxCSS(self):
        fontFamily, size = REsplit(",", self.fontSelection)
        fontFamily = fontFamily.strip()
        fontSize = size.strip()
        self.fontPreviewBox.setStyleSheet(_fromUtf8("color: %s; font: %spt \"%s\"; background-color: %s;" % (self.fgColorSelector.currentColor, fontSize, fontFamily, self.bgColorSelector.currentColor)))

    def colorPopup(self, startColor="#FFFFFF"):
        #Create the color dialog object
        color = QtGui.QColorDialog()
        #create the QTimer and connect its timeout() signal to a function that sets the color dialog to be topmost
        #We have to do it this way because normally the QColorDialog halts the current thread.
        #The only way to set the window top-most is to set it this way from a different thread.
        #QTimer facilitates this on a basic level without needing to fuss with complex QThreads.
        self.timer = QtCore.QTimer()
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.forceColorDialogOnTop)
        self.timer.start(25)
        #Create a QColor object for the startColor
        propColor = QtGui.QColor()
        propColor.setNamedColor(startColor)
        #Now we open the color dialog and get the color, returning it as selectedColor which is a QColor object.
        selectedColor = color.getColor(propColor)
        if selectedColor.isValid():
            return selectedColor.name()
        else:
            return startColor


    def selectBgColor(self):
        bgColor = self.colorPopup(self.bgColorSelector.currentColor)
        self.bgColorSelector.currentColor = bgColor
        self.bgColorSelector.setStyleSheet(_fromUtf8("background-color: %s;" % (bgColor)))
        self.updatePreviewBoxCSS()

    def selectFgColor(self):
        fgColor = self.colorPopup(self.fgColorSelector.currentColor)
        self.fgColorSelector.currentColor = fgColor
        self.fgColorSelector.setStyleSheet(_fromUtf8("background-color: %s;" % (fgColor)))
        self.updatePreviewBoxCSS()

    def forceColorDialogOnTop(self):
        #Kind of a nasty hack here. The QColorDialog seems to be impossible to open on top of all other windows.
        #So we have to manually set the window position using win32gui and win32con
        if self.AOT is True:
            cpHandle = win32gui.FindWindow(None, "Select Color")
            cpPos = win32gui.GetWindowRect(cpHandle)
            win32gui.SetWindowPos(cpHandle, win32con.HWND_TOPMOST, cpPos[0], cpPos[1], int(cpPos[2]-cpPos[0]), int(cpPos[3]-cpPos[1]), 0)
        #Kill the timer
        self.timer.stop()

    def forceFontDialogOnTop(self):
        if self.AOT is True:
            cpHandle = win32gui.FindWindow(None, "Select Font")
            cpPos = win32gui.GetWindowRect(cpHandle)
            win32gui.SetWindowPos(cpHandle, win32con.HWND_TOPMOST, cpPos[0], cpPos[1], int(cpPos[2]-cpPos[0]), int(cpPos[3]-cpPos[1]), 0)
        #Kill the timer
        self.timer.stop()


    def popupLogSavePath(self):
        fileDialog = QtGui.QFileDialog()
        #fileDialog.AcceptMode = 1
        fileDialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        chosenFile = fileDialog.getExistingDirectory(caption="Choose where to save debug output...", directory=_SETDIR)
        self.folderPathText.setText(_translate("OptionsDialog", chosenFile, None))

    def retranslateUi(self, OptionsDialog):
        OptionsDialog.setWindowTitle(_translate("OptionsDialog", "Options", None))


        #FIRST TAB - APPEARANCE
        self.fontSelectionGroup.setTitle(_translate("OptionsDialog", "Font", None))
        self.fontSelectionTextbox.setText(_translate("OptionsDialog", "Tahoma, 8", None))
        self.selectFontButton.setText(_translate("OptionsDialog", "Select Font", None))
        self.colorSelectionGroup.setTitle(_translate("OptionsDialog", "Colors", None))
        self.bgColorLabel.setText(_translate("OptionsDialog", "Background: ", None))
        self.fgColorLabel.setText(_translate("OptionsDialog", "Foreground: ", None))
        self.fgColorSelector.setStyleSheet(_fromUtf8("background-color: #FFFFFF;"))
        self.bgColorSelector.setStyleSheet(_fromUtf8("background-color: #000000;"))
        self.fontPreviewLabel.setText(_translate("OptionsDialog", "Font Preview", None))
        self.fontPreviewBox.setStyleSheet(_fromUtf8("color: rgb(0, 0, 0); font: 8pt \"Tahoma\"; background-color: rgb(255, 255, 255);"))
        self.optionsTabContainer.setTabText(self.optionsTabContainer.indexOf(self.tab_Appearance), _translate("OptionsDialog", "Appearance", None))
        ##END FIRST TAB - APPEARANCE ##


        #SECOND TAB - FOOBAR2K SERVER INFO
        self.addressPortGroup.setTitle(_translate("OptionsDialog", "Address and port", None))
        self.addressInput.setText(_translate("OptionsDialog", "127.0.0.1", None))
        self.colonLabel.setText(_translate("OptionsDialog", ":", None))
        self.portTextInput.setText(_translate("OptionsDialog", "8888", None))
        self.reqCredsCheck.setText(_translate("OptionsDialog", "Requires username/password?", None))
        self.credentialsGroup.setTitle(_translate("OptionsDialog", "Credentials", None))
        self.usernameLabel.setText(_translate("OptionsDialog", "Username:  ", None))
        self.passwordLabel.setText(_translate("OptionsDialog", "Password:  ", None))

        self.optionsTabContainer.setTabText(self.optionsTabContainer.indexOf(self.tab_WebInterface), _translate("OptionsDialog", "Foobar2k Server Info", None))
        ## END SECOND TAB - FOOBAR2K SERVER INFO ##


        #THIRD TAB - ADVANCED
        self.debugGroup.setTitle(_translate("OptionsDialog", "Debug Mode", None))
        self.debugWriteCheck.setText(_translate("OptionsDialog", "Write extra info to disk", None))
        self.debugEnabledCheck.setText(_translate("OptionsDialog", "Enabled", None))
        self.selectFolderGroup.setTitle(_translate("OptionsDialog", "Select output folder", None))
        self.folderPathText.setText(_translate("OptionsDialog", _CURDIR, None))
        self.browseButton.setText(_translate("OptionsDialog", "Browse", None))
        self.internalStuffGroup.setTitle(_translate("OptionsDialog", "Internal Stuff", None))
        self.alwaysOnTopCheck.setToolTip(_translate("OptionsDialog", "This will cause the application to be \'pinned\' above all other windows. <b><u>Requires Restart</u></b>", None))
        self.alwaysOnTopCheck.setText(_translate("OptionsDialog", "Always On Top", None))
        self.MRLabel.setToolTip(_translate("OptionsDialog", "This is the master ratio for the <br>probabilistic matcher which is used when searching for lyrics. This ratio determines how close of a match is acceptable when comparing artist and song title against the search results.", None))
        self.MRLabel.setText(_translate("OptionsDialog", "Master Match Ratio:", None))
        self.MRSelector.setToolTip(_translate("OptionsDialog", "This is the master ratio for the <br>probabilistic matcher which is used when searching for lyrics. This ratio determines how close of a match is acceptable when comparing artist and song title against the search results.", None))
        self.optionsTabContainer.setTabText(self.optionsTabContainer.indexOf(self.tab_Advanced), _translate("OptionsDialog", "Advanced", None))
        ## END THIRD TAB - ADVANCED ##

        self.resetButton.setText(_translate("OptionsDialog", "Reset", None))
