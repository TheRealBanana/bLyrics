from PyQt4 import QtCore, QtGui

class lyricsSearchFunctions(object):
    def __init__(self, searchDialog):
        self.searchDialog = searchDialog
        self.setupConnections()

    def setupConnections(self):
        QtCore.QObject.connect(self.searchDialog.searchButton, QtCore.SIGNAL("clicked()"), self.searchButtonClicked)
        QtCore.QObject.connect(self.searchDialog.leftTabWidget_Results, QtCore.SIGNAL("tabCloseRequested(int)"), self.closeTab)

    def searchButtonClicked(self):
        #Do nothing for no-input searches
        if len(self.searchDialog.songNameInput.text()) + len(self.searchDialog.artistNameInput.text()) + len(self.searchDialog.lyricsSearchStringInput.text()) == 0:
            return
        #The basic idear is this:
        #On click we create a new search results tab and start to populate it with answers
        #This population should be done with QThread if possible
        #During population (searching) we need to disable the tabwidget
        #We also change the search button to a cancel button
        #
        #or
        #
        #Instead of locking the UI (disableing the tabwidget) we can create a population thread and then connection
        #slots inside that specific thread to slots for the specific QListWidget for the search tab we created.
        #Then a user can change tabs if they want and the correct widget will still be updated with search results
        #
        #The second idea allows multiple searches at once and is generally less intrusive to the user (I think).

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
        verticallayout.addWidget(resultsListWidget)
        resultsListWidget.addItem("Test Item 1 %s " % str(newtabindex+1))
        resultsListWidget.addItem("Test Item 2 %s " % str(newtabindex+1))
        #Thought about using the actual search parameters for the tab title but it becomes difficult to access
        #the tabs when their titles are too long. This works fine for what we need.
        tabtitle = "Search Query %s" % str(newtabindex+1)
        self.searchDialog.leftTabWidget_Results.addTab(newtab, tabtitle)
        self.searchDialog.leftTabWidget_Results.setCurrentIndex(newtabindex)


    def closeTab(self, tabIndex):
        #Deleting the main widget should clean up any connections we made to it and its sub-widgets
        self.searchDialog.leftTabWidget_Results.widget(tabIndex).deleteLater()
        self.searchDialog.leftTabWidget_Results.removeTab(tabIndex)
