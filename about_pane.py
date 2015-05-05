#about_pane.py - by Kyle Claisse - 2013
#
# encoding: utf-8

# Form implementation generated from reading ui file 'about_pane.ui'
#
# Created: Tue May 28 03:19:28 2013
#	  by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!
#
#
# Last Modified: July 24, 2014
#

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


_PROGRAM_VER_ = "0.707b0 (W.I.P.) Experimental"

class Ui_aboutWindow(object):
	def setupUi(self, aboutWindow):
		width = 270
		height = 175
		aboutWindow.setObjectName(_fromUtf8("aboutWindow"))
		aboutWindow.resize(width, height)
		aboutWindow.setMinimumSize(QtCore.QSize(width, height))
		aboutWindow.setMaximumSize(QtCore.QSize(width, height))
		aboutWindow.setStyleSheet(_fromUtf8("background-color: rgb(250, 250, 250);"))
		self.aboutBox = QtGui.QTextBrowser(aboutWindow)
		self.aboutBox.setGeometry(QtCore.QRect(9, 9, 252, 197))
		self.aboutBox.setStyleSheet(_fromUtf8("background-color: rgb(250, 250, 250);"))
		self.aboutBox.setFrameShape(QtGui.QFrame.NoFrame)
		self.aboutBox.setFrameShadow(QtGui.QFrame.Plain)
		self.aboutBox.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
		self.aboutBox.setObjectName(_fromUtf8("aboutBox"))
		self.closeButton = QtGui.QPushButton(aboutWindow)
		self.closeButton.setGeometry(QtCore.QRect(180, 140, 80, 23))
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.closeButton.sizePolicy().hasHeightForWidth())
		self.closeButton.setSizePolicy(sizePolicy)
		self.closeButton.setObjectName(_fromUtf8("closeButton"))

		self.retranslateUi(aboutWindow)
		QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), aboutWindow.close)
		QtCore.QMetaObject.connectSlotsByName(aboutWindow)

	def retranslateUi(self, aboutWindow):
		aboutWindow.setWindowTitle(_translate("aboutWindow", "About bLyrics", None))
		self.aboutBox.setHtml(_translate("aboutWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">bLyrics v" + _PROGRAM_VER_ + "</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">(Written by Kyle Claisse)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">This is an application written in python with the help of PyQt4. It makes use of foobar2000\'s COM interface plugin as well as the web interface plugin to display the current status. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">The lyrics are provided by LyricsWiki and songlyrics.com. </span></p></body></html>", None))
		self.closeButton.setText(_translate("aboutWindow", "Close", None))

