import os.path
from PyQt4 import QtCore, QtGui
from difflib import SequenceMatcher as sMatcher
import re
from base64 import urlsafe_b64decode
from lyrics_cacher import LyricsCacher, FILEEXTENSION, CACHEWRITEFOLDER

MASTER_RATIO = 0.65
START_HIGHLIGHT = '<span style="background-color: #FFFF00">'
END_HIGHLIGHT = "</span>"
#START_HIGHLIGHT = "<b>"
#END_HIGHLIGHT = "</b>"

class searchJob(QtCore.QObject):
    def __init__(self, pagereference, searchparams, filelist):
        self.pagereference = pagereference
        self.filelist = filelist
        self.searchparams = searchparams
        self.quitting = False
        super(searchJob, self).__init__()

    def startSearch(self):
        idx = 0
        while self.quitting is False and idx < len(self.filelist):
            b64part = self.filelist[idx][:-len(FILEEXTENSION)]
            decoded = urlsafe_b64decode(b64part)
            artist, song = re.split("___", decoded)
            #Reading the inside of every file is going to be slow so we throw out results by their filename when we can
            #Ignore any songs that don't match our song/artist parameters (if we have them)
            if len(self.searchparams["song"]) > 0:
                if sMatcher(None, str(self.searchparams["song"]).lower(), song.lower()).ratio() < MASTER_RATIO:
                    idx += 1
                    continue

            if len(self.searchparams["artist"]) > 0:
                if sMatcher(None, str(self.searchparams["artist"]).lower(), artist.lower()).ratio() < MASTER_RATIO:
                    idx += 1
                    continue

            #If we got this far that means our song/artist must have either matched or werent included.
            #We need to load the lyrics for this song. If we have a searchString in our search params will
            #test for that now. If we don't, we just add this to the results.
            lyricsfilepath = os.path.join(CACHEWRITEFOLDER, self.filelist[idx])
            with open(lyricsfilepath, 'r') as lyricsfile:
                lyrics = unicode(lyricsfile.read()).decode("utf8")
            #Match our substring, going with exact matches cause using our SequenceMatcher against every single word
            #in the lyrics sounds like a very bad idea but we may investigate it later if required.
            if len(self.searchparams["searchString"]) > 0:
                if str(self.searchparams["searchString"]).lower() not in lyrics.lower():
                    idx += 1
                    continue
                else:
                    #Highlight our search string and fix line breaks
                    hledstring = START_HIGHLIGHT + str(self.searchparams["searchString"]) + END_HIGHLIGHT
                    lyrics = re.sub(re.escape(str(self.searchparams["searchString"])), hledstring, lyrics, flags=re.I)
                    lyrics = re.sub("\n", "<br>", lyrics)

            #If we got this far we have a good match, lets add it to our page reference.
            listentryitem = QtGui.QListWidgetItem("%s by %s" % (song, artist))
            listentryitem.setData(QtCore.Qt.UserRole, lyrics)
            listwidgetref = self.pagereference.findChild(QtGui.QListWidget, "resultsListWidget")
            listwidgetref.addItem(listentryitem)

            QtGui.QApplication.processEvents()
            idx += 1

        self.emit(QtCore.SIGNAL("SearchFinished"))


class lyricsSearchFunctions(object):
    def __init__(self, searchDialog):
        self.searchDialog = searchDialog
        self.searchThread = None
        self.searchJobTask = None
        self.activeSearchJobWidget = None
        self.lyricsCacherRef = LyricsCacher()
        self.setupConnections()

    def setupConnections(self):
        QtCore.QObject.connect(self.searchDialog.searchButton, QtCore.SIGNAL("clicked()"), self.searchButtonClicked)
        QtCore.QObject.connect(self.searchDialog.leftTabWidget_Results, QtCore.SIGNAL("tabCloseRequested(int)"), self.closeTab)

    def cancelSearchJob(self):
        if self.searchThread is not None:
            self.searchJobTask.quitting = True
            self.searchThread.quit()
            self.searchThread.wait()
            if self.searchJobTask is not None:
                QtCore.QObject.disconnect(self.searchThread, QtCore.SIGNAL("started()"), self.searchJobTask.startSearch)
                QtCore.QObject.disconnect(self.searchJobTask, QtCore.SIGNAL("workFinished()"), self.searchThread.quit)
                QtCore.QObject.disconnect(self.searchJobTask, QtCore.SIGNAL("SearchFinished"), self.searchJobFinished)
        self.activeSearchJobWidget = None
        QtCore.QObject.disconnect(self.searchDialog.searchButton, QtCore.SIGNAL("clicked()"), self.cancelSearchJob)
        QtCore.QObject.connect(self.searchDialog.searchButton, QtCore.SIGNAL("clicked()"), self.searchButtonClicked)
        self.searchDialog.searchButton.setText("Search Lyrics Cache")

    def searchJobFinished(self):
        print "Search complete!"
        self.cancelSearchJob()

    def listItemClicked(self, listWidgetItem):
        self.searchDialog.resultLyricsView.setHtml(listWidgetItem.data(QtCore.Qt.UserRole).toPyObject())

    def createSearchJob(self, pagereference):
        #Gather our search parameters
        searchparams = {}
        searchparams["song"] = self.searchDialog.songNameInput.text()
        searchparams["artist"] = self.searchDialog.artistNameInput.text()
        searchparams["searchString"] = self.searchDialog.lyricsSearchStringInput.text()
        self.searchThread = QtCore.QThread()
        self.searchJobTask = searchJob(pagereference, searchparams, self.lyricsCacherRef.getLyricsFileList())
        self.searchJobTask.moveToThread(self.searchThread)
        QtCore.QObject.connect(self.searchThread, QtCore.SIGNAL("started()"), self.searchJobTask.startSearch)
        QtCore.QObject.connect(self.searchJobTask, QtCore.SIGNAL("workFinished()"), self.searchThread.quit)
        QtCore.QObject.connect(self.searchJobTask, QtCore.SIGNAL("SearchFinished"), self.searchJobFinished)
        self.searchThread.start()
        self.activeSearchJobWidget = pagereference
        #Swap our search button to a cancel button
        QtCore.QObject.disconnect(self.searchDialog.searchButton, QtCore.SIGNAL("clicked()"), self.searchButtonClicked)
        QtCore.QObject.connect(self.searchDialog.searchButton, QtCore.SIGNAL("clicked()"), self.cancelSearchJob)
        self.searchDialog.searchButton.setText("Cancel Search")

    def searchButtonClicked(self):
        #Do nothing for no-input searches
        if len(self.searchDialog.songNameInput.text()) + len(self.searchDialog.artistNameInput.text()) + len(self.searchDialog.lyricsSearchStringInput.text()) == 0:
            return

        #Each result tab is a vertical layout with a Qlabel at the top and a QListWidget below that with our results.
        #QLabel at the top will contain the search parameters
        newtab = QtGui.QWidget()
        newtabindex = self.searchDialog.leftTabWidget_Results.count()
        verticallayout = QtGui.QVBoxLayout(newtab)
        searchParamsLabel = QtGui.QLabel(newtab)
        searchParamsLabel.setObjectName("searchParamsLabel")
        searchParamsLabel.setMinimumHeight(15)
        searchParamsLabel.setMaximumHeight(40)
        searchParamsLabel.setWordWrap(True)
        searchParamsLabel.setText("Song: '%s'  -  Artist: '%s'  -  Search String: '%s'" % (self.searchDialog.songNameInput.text(), self.searchDialog.artistNameInput.text(), self.searchDialog.lyricsSearchStringInput.text()))
        verticallayout.addWidget(searchParamsLabel)
        resultsListWidget = QtGui.QListWidget(newtab)
        resultsListWidget.setObjectName("resultsListWidget")
        resultsListWidget.setSortingEnabled(False)
        #This signal should be deleted when the page is deleted so we don't need to worry about disconnecting
        QtCore.QObject.connect(resultsListWidget, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.listItemClicked)
        verticallayout.addWidget(resultsListWidget)
        #Thought about using the actual search parameters for the tab title but it becomes difficult to access
        #the tabs when their titles are too long. This works fine for what we need.
        tabtitle = "Search Query %s" % str(newtabindex+1)
        self.searchDialog.leftTabWidget_Results.addTab(newtab, tabtitle)
        self.searchDialog.leftTabWidget_Results.setCurrentIndex(newtabindex)
        self.createSearchJob(newtab)

    def closeTab(self, tabIndex):
        #Dont allow closing a tab with a search job active on it
        activeSearchJobTabIndex = self.searchDialog.leftTabWidget_Results.indexOf(self.activeSearchJobWidget)
        if tabIndex != activeSearchJobTabIndex:
            #Deleting the main widget should clean up any connections we made to it and its sub-widgets
            self.searchDialog.leftTabWidget_Results.widget(tabIndex).deleteLater()
            self.searchDialog.leftTabWidget_Results.removeTab(tabIndex)

    def closeDialog(self):
        self.cancelSearchJob()