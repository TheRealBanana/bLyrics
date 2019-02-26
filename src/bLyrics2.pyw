from dialogs.blyrics_ui import Ui_MainWindow
from dialogs.logic.blyrics_ui_functions import UIFunctions
from PyQt4 import QtGui, QtCore
import sys

#Set default encoding to utf8
#Ima get this unicode problem under wraps eventually...
reload(sys)
sys.setdefaultencoding('utf8')

#Trying something new with the stdout,stderr so I can see it in both the cmdline and UI console.
class OUTMETHODS(object):
    def __init__(self, MainWindowRef):
        self.console_out = True
        self.cmd_out = False if "pythonw" in sys.executable else True
        self.MainWindowRef = MainWindowRef
        self.stdout = self.STDOUT(self)
        self.stderr = self.STDERR(self)

    def writeout(self, mode, text):
        if self.console_out:
            self.MainWindowRef.emit(QtCore.SIGNAL("consoleWrite"), text)
        if self.cmd_out:
            if mode == "stdout":
                sys.__stdout__.write(text)
            if mode == "stderr":
                sys.__stderr__.write(text)

    class STDOUT(object):
        def __init__(self, parent): self.parent = parent
        def write(self, text):
            self.parent.writeout("stdout", text)

    class STDERR(object):
        def __init__(self, parent): self.parent = parent
        def write(self, text):
            self.parent.writeout("stderr", text)


#If we had any other dialogs open, like the cache builder or the search window, we wouldn't actually close
#This fixes that issue.
class ClosableMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ClosableMainWindow, self).__init__(parent)

    def closeEvent(self, closeEvent):
        self.emit(QtCore.SIGNAL("MainWindowClose"))
        closeEvent.accept()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = ClosableMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    uifuncts = UIFunctions(ui)

    #Set up our standard out and error before setting up the UI
    outfuncs = OUTMETHODS(MainWindow)
    QtCore.QObject.connect(MainWindow, QtCore.SIGNAL("consoleWrite"), uifuncts.write)

    sys.stdout = outfuncs.stdout
    sys.stderr = outfuncs.stderr


    # Hook into the app's quiting sequence so it saves our settings before it quits
    QtCore.QObject.connect(MainWindow, QtCore.SIGNAL("MainWindowClose"), uifuncts.quitApp)

    #Now that we have the Ui set up, lets finish the initiation process
    uifuncts.appInit()
    # Set always-on-top if the user wants it
    if uifuncts.loadedOptions["Advanced"]["alwaysOnTop"]:
        MainWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    MainWindow.show()
    app.exec_()