from PyQt4 import QtCore, QtGui
from os.path import basename

class Ui_fakeCellWidget(QtGui.QWidget):
    def __init__(self, rowData, parent=None):
        super(Ui_fakeCellWidget, self).__init__(parent)
        self.setObjectName("fakeCellWidget")
        self.resize(477, 17)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMaximumSize(QtCore.QSize(16777215, 17))
        #self.setStyleSheet("background-color: rgb(200, 200, 200);")
        self.horizontalLayout = QtGui.QHBoxLayout(self)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.rowNumber = QtGui.QLabel(self)
        self.rowNumber.setMinimumSize(QtCore.QSize(20, 17))
        self.rowNumber.setMaximumSize(QtCore.QSize(20, 17))
        self.rowNumber.setFrameShape(QtGui.QFrame.StyledPanel)
        self.rowNumber.setAlignment(QtCore.Qt.AlignCenter)
        self.rowNumber.setObjectName("rowNumber")
        self.horizontalLayout.addWidget(self.rowNumber)

        self.column1 = QtGui.QLabel(self)
        self.column1.setMinimumSize(QtCore.QSize(100, 17))
        self.column1.setMaximumSize(QtCore.QSize(100, 17))
        self.column1.setFrameShape(QtGui.QFrame.StyledPanel)
        self.column1.setAlignment(QtCore.Qt.AlignCenter)
        self.column1.setObjectName("column1")
        self.horizontalLayout.addWidget(self.column1)

        self.column2 = QtGui.QLabel(self)
        self.column2.setMinimumSize(QtCore.QSize(50, 17))
        self.column2.setMaximumSize(QtCore.QSize(50, 17))
        self.column2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.column2.setAlignment(QtCore.Qt.AlignCenter)
        self.column2.setObjectName("column2")
        self.horizontalLayout.addWidget(self.column2)

        self.column3 = QtGui.QLabel(self)
        self.column3.setMaximumSize(QtCore.QSize(16777215, 17))
        self.column3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.column3.setAlignment(QtCore.Qt.AlignCenter)
        self.column3.setObjectName("column3")
        self.horizontalLayout.addWidget(self.column3)

        #rowData[0] = Lyrics provider name
        #rowData[1] = provider version
        #rowData[2] = file path (make sure to add tool hint with full path and use just hte filename in the GUI)
        #rowData[3] = list index (based on priority, maybe just straight priority)
        self.rowNumber.setText(rowData[3])
        self.column1.setText(rowData[0])
        self.column1.setToolTip(rowData[0])
        self.column2.setText(rowData[1])
        self.column2.setToolTip(rowData[1])
        self.column3.setText(basename(rowData[2]))
        self.column3.setToolTip(rowData[2])