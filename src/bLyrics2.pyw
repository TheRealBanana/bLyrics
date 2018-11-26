from dialogs.blyrics_ui import *
from PyQt4 import QtGui, QtCore
import sys

#Set default encoding to utf8
#Ima get this unicode problem under wraps eventually...
reload(sys)
sys.setdefaultencoding('utf8')

#Trying something new with the stdout,stderr so I can see it in both the cmdline and UI console.
class OUTMETHODS(object):
    def __init__(self, MainWindowRef, stdoutfunc, stderrfunc):
        self.console_out = True
        self.cmd_out = True
        self.MainWindowRef = MainWindowRef
        self.stdout = self.STDOUT(self)
        self.stderr = self.STDERR(self)
        self.stdoutfunc = stdoutfunc
        self.stderrfunc = stderrfunc

    def writeout(self, mode, text):
        if self.console_out:
            self.MainWindowRef.emit(QtCore.SIGNAL("consoleWrite"), text)
        if self.cmd_out:
            if mode == "stdout":
                self.stdoutfunc.write(text)
            if mode == "stderr":
                self.stderrfunc.write(text)

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
    ui = Ui_MainWindow(MainWindow)
    #Set up our standard out and error before setting up the UI
    outfuncs = OUTMETHODS(MainWindow, sys.stdout, sys.stderr)
    QtCore.QObject.connect(MainWindow, QtCore.SIGNAL("consoleWrite"), ui.UiFunctions.write)

    out = outfuncs.stdout
    err = outfuncs.stderr
    sys.stdout = out
    sys.stderr = err
    ui.setupUi()

    # Hook into the app's quiting sequence so it saves our settings before it quits
    QtCore.QObject.connect(MainWindow, QtCore.SIGNAL("MainWindowClose"), ui.UiFunctions.quitApp)

    # Before we get going we get the user setting for _ALWAYS_ON_TOP
    _ALWAYS_ON_TOP_ = False
    if ui.UiFunctions.testSettingGroup("Options") is True:
        rd = {"Advanced": ["alwaysOnTop"]}
        if ui.UiFunctions.loadSettings(optionsMenu=True, data=rd)["Advanced"][0] == "true":
            _ALWAYS_ON_TOP_ = True
    # Set always-on-top if the user wants it
    if _ALWAYS_ON_TOP_:
        MainWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    MainWindow.show()
    app.exec_()