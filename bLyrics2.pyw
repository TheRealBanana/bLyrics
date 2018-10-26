from blyrics_ui import *
from blyrics_ui_functions import _ALWAYS_ON_TOP_
from PyQt4 import QtGui
import sys


#Trying something new with the stdout,stderr so I can see it in both the cmdline and UI console.
class OUTMETHODS(object):
    def __init__(self, console_write_func, stdoutfunc, stderrfunc):
        self.console_out = True
        self.cmd_out = True
        self.console_write_func = console_write_func
        self.stdout = self.STDOUT(self)
        self.stderr = self.STDERR(self)
        self.stdoutfunc = stdoutfunc
        self.stderrfunc = stderrfunc

    def writeout(self, mode, text):
        if self.console_out: self.console_write_func(text)
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



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    #Set up our standard out and error before setting up the UI
    outfuncs = OUTMETHODS(ui.UiFunctions.write, sys.stdout, sys.stderr)
    out = outfuncs.stdout
    err = outfuncs.stderr
    sys.stdout = out
    sys.stderr = err
    ui.setupUi()
    # Hook into the app's quiting sequence so it saves our settings before it quits
    app.aboutToQuit.connect(ui.UiFunctions.saveSettings)
    # Before we get going we get the user setting for _ALWAYS_ON_TOP
    if ui.UiFunctions.testSettingGroup("Options") is True:
        rd = {"Advanced": ["alwaysOnTop"]}
        if ui.UiFunctions.loadSettings(optionsMenu=True, data=rd)["Advanced"][0] == "true":
            _ALWAYS_ON_TOP_ = True
    # Set always-on-top if the user wants it
    if _ALWAYS_ON_TOP_:
        MainWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    MainWindow.show()

    sys.exit(app.exec_())