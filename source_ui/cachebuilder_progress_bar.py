# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cachebuilder_progress_bar.ui'
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

class Ui_cachebuilderProgressDialog(object):
    def setupUi(self, cachebuilderProgressDialog):
        cachebuilderProgressDialog.setObjectName(_fromUtf8("cachebuilderProgressDialog"))
        cachebuilderProgressDialog.resize(298, 123)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(cachebuilderProgressDialog.sizePolicy().hasHeightForWidth())
        cachebuilderProgressDialog.setSizePolicy(sizePolicy)
        cachebuilderProgressDialog.setMinimumSize(QtCore.QSize(298, 123))
        cachebuilderProgressDialog.setMaximumSize(QtCore.QSize(16777215, 123))
        self.verticalLayout = QtGui.QVBoxLayout(cachebuilderProgressDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.progressBar = QtGui.QProgressBar(cachebuilderProgressDialog)
        self.progressBar.setTextVisible(False)
        self.progressBar.setFormat(_fromUtf8("%p%"))
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.progressLabel = QtGui.QLabel(cachebuilderProgressDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressLabel.sizePolicy().hasHeightForWidth())
        self.progressLabel.setSizePolicy(sizePolicy)
        self.progressLabel.setMinimumSize(QtCore.QSize(280, 0))
        self.progressLabel.setMaximumSize(QtCore.QSize(1500, 16777215))
        self.progressLabel.setTextFormat(QtCore.Qt.PlainText)
        self.progressLabel.setObjectName(_fromUtf8("progressLabel"))
        self.verticalLayout.addWidget(self.progressLabel)
        self.centeredCancelButton = QtGui.QFrame(cachebuilderProgressDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centeredCancelButton.sizePolicy().hasHeightForWidth())
        self.centeredCancelButton.setSizePolicy(sizePolicy)
        self.centeredCancelButton.setMinimumSize(QtCore.QSize(205, 40))
        self.centeredCancelButton.setMaximumSize(QtCore.QSize(16777215, 40))
        self.centeredCancelButton.setObjectName(_fromUtf8("centeredCancelButton"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centeredCancelButton)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cancelButton = QtGui.QPushButton(self.centeredCancelButton)
        self.cancelButton.setMinimumSize(QtCore.QSize(75, 22))
        self.cancelButton.setMaximumSize(QtCore.QSize(75, 22))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        spacerItem1 = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.centeredCancelButton)

        self.retranslateUi(cachebuilderProgressDialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), cachebuilderProgressDialog.close)
        QtCore.QMetaObject.connectSlotsByName(cachebuilderProgressDialog)

    def retranslateUi(self, cachebuilderProgressDialog):
        cachebuilderProgressDialog.setWindowTitle(_translate("cachebuilderProgressDialog", "Dialog", None))
        self.progressLabel.setText(_translate("cachebuilderProgressDialog", "_STATUS_TEXT_", None))
        self.cancelButton.setText(_translate("cachebuilderProgressDialog", "Cancel", None))

