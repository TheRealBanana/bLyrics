from PyQt4 import QtCore, QtGui
from difflib import SequenceMatcher
import re

MASTER_RATIO = 0.80
START_HIGHLIGHT = '<span style="background-color: #FFFF00">'
END_HIGHLIGHT = "</span>"
#START_HIGHLIGHT = "<b>"
#END_HIGHLIGHT = "</b>"


#This function is just superb and I know I couldn't do any better.
#Thanks so much to Ulf Aslak for this
#https://stackoverflow.com/questions/36013295/find-best-substring-match/36132391#36132391
def get_best_match(query, corpus, step=4, flex=3, case_sensitive=False, verbose=False):
    """Return best matching substring of corpus.

    Parameters
    ----------
    query : str
    corpus : str
    step : int
        Step size of first match-value scan through corpus. Can be thought of
        as a sort of "scan resolution". Should not exceed length of query.
    flex : int
        Max. left/right substring position adjustment value. Should not
        exceed length of query / 2.

    Outputs
    -------
    output0 : str
        Best matching substring.
    output1 : float
        Match ratio of best matching substring. 1 is perfect match.
    """

    def _match(a, b):
        """Compact alias for SequenceMatcher."""
        return SequenceMatcher(None, a, b).ratio()

    def scan_corpus(step):
        """Return list of match values from corpus-wide scan."""
        match_values = []

        m = 0
        while m + qlen - step <= len(corpus):
            match_values.append(_match(query, corpus[m : m-1+qlen]))
            if verbose:
                print query, "-", corpus[m: m + qlen], _match(query, corpus[m: m + qlen])
            m += step

        return match_values

    def index_max(v):
        """Return index of max value."""
        return max(xrange(len(v)), key=v.__getitem__)

    def adjust_left_right_positions():
        """Return left/right positions for best string match."""
        # bp_* is synonym for 'Best Position Left/Right' and are adjusted
        # to optimize bmv_*
        p_l, bp_l = [pos] * 2
        p_r, bp_r = [pos + qlen] * 2

        # bmv_* are declared here in case they are untouched in optimization
        bmv_l = match_values[p_l / step]
        bmv_r = match_values[p_l / step]

        for f in range(flex):
            ll = _match(query, corpus[p_l - f: p_r])
            if ll > bmv_l:
                bmv_l = ll
                bp_l = p_l - f

            lr = _match(query, corpus[p_l + f: p_r])
            if lr > bmv_l:
                bmv_l = lr
                bp_l = p_l + f

            rl = _match(query, corpus[p_l: p_r - f])
            if rl > bmv_r:
                bmv_r = rl
                bp_r = p_r - f

            rr = _match(query, corpus[p_l: p_r + f])
            if rr > bmv_r:
                bmv_r = rr
                bp_r = p_r + f

        return bp_l, bp_r, _match(query, corpus[bp_l : bp_r])

    if not case_sensitive:
        query = query.lower()
        corpus = corpus.lower()

    qlen = len(query)

    match_values = scan_corpus(step)
    if len(match_values) == 0:
        return 0, 0, 0.0
    pos = index_max(match_values) * step

    pos_left, pos_right, match_value = adjust_left_right_positions()

    return corpus[pos_left: pos_right].strip(), match_value

class searchJob(QtCore.QObject):
    def __init__(self, pagereference, searchparams, cacheref):
        self.pagereference = pagereference
        self.searchparams = searchparams
        self.cacheref = cacheref
        self.quitting = False
        super(searchJob, self).__init__()

    def updateProgress(self, idx, total):
        self.emit(QtCore.SIGNAL("SearchCountUpdate"), idx, total)
        QtGui.QApplication.processEvents()

    def startSearch(self):
        # Make sure we're dealing with unicode.
        if not isinstance(self.searchparams["song"], unicode): self.searchparams["song"] = unicode(self.searchparams["song"], "utf-8")
        if not isinstance(self.searchparams["artist"], unicode): self.searchparams["artist"] = unicode(self.searchparams["artist"], "utf-8")
        if not isinstance(self.searchparams["searchString"], unicode): self.searchparams["searchString"] = unicode(self.searchparams["searchString"], "utf-8")
        searchedsong = self.searchparams["song"]
        searchedartist = self.searchparams["artist"]
        searchedstring = self.searchparams["searchString"]

        #Any unchecked exact checkbox means we have to pull all entries for that field (set query to %).
        #Anything exact we still pad with wildcards just to be sure
        if self.searchparams["exactMatch_Artist"] == 0 or len(searchedartist) == 0:
            searchedartist = "%"
        else:
            searchedartist = "%%%s%%" % searchedartist
        if self.searchparams["exactMatch_Song"] == 0 or len(searchedsong) == 0:
            searchedsong = "%"
        else:
            searchedsong = "%%%s%%" % searchedsong
        if self.searchparams["exactMatch_SearchString"] == 0 or len(searchedstring) == 0:
            searchedstring = "%"
        else:
            searchedstring = "%%%s%%" % searchedstring

        results = self.cacheref.searchLyricsCache(searchedsong, searchedartist, searchedstring)
        #Swap anything we changed back for further filtering below
        searchedsong = self.searchparams["song"]
        searchedartist = self.searchparams["artist"]
        searchedstring = self.searchparams["searchString"]

        total = len(results)
        for idx, r in enumerate(results):
            self.updateProgress(idx, total)
            if self.quitting is True:
                break
            song, artist = r
            lyrics = self.cacheref.getLyrics(song, artist)
            #Inexact searching for artist and song
            if searchedartist.lower() not in artist.lower() and SequenceMatcher(None, searchedartist.lower(), artist.lower()).ratio() < MASTER_RATIO:
                continue
            if searchedsong.lower() not in song.lower() and SequenceMatcher(None, searchedsong.lower(), song.lower()).ratio() < MASTER_RATIO:
                continue

            if len(searchedstring) > 0 and searchedstring != "%":
                replstring = searchedstring
                if self.searchparams["exactMatch_SearchString"] == 0:
                    good_match = get_best_match(searchedstring, lyrics)
                    if good_match[1] > MASTER_RATIO:
                        replstring = good_match[0]
                    else:
                        continue
                elif searchedstring.lower() not in lyrics.lower():
                    continue

                #Highlight our search string and fix line breaks
                hledstring = START_HIGHLIGHT + replstring + END_HIGHLIGHT
                lyrics = re.sub(re.escape(replstring), hledstring, lyrics, flags=re.I)

            lyrics = re.sub("\n", "<br>", lyrics)
            entrytitle = "%s by %s" % (unicode(song).decode("utf8"), unicode(artist).decode("utf8"))
            listentryitem = QtGui.QListWidgetItem(entrytitle)
            listentryitem.setData(QtCore.Qt.ToolTipRole, entrytitle)
            listentryitem.setData(QtCore.Qt.UserRole, lyrics)
            listwidgetref = self.pagereference.findChild(QtGui.QListWidget, "resultsListWidget")
            listwidgetref.addItem(listentryitem)

        self.emit(QtCore.SIGNAL("SearchFinished"))


class lyricsSearchFunctions(object):
    def __init__(self, searchDialog, lyricsCacheRef):
        self.searchDialog = searchDialog
        self.searchThread = None
        self.searchJobTask = None
        self.activeSearchJobWidget = None
        self.lyricsCacherRef = lyricsCacheRef
        self.cachesize = str(self.lyricsCacherRef.getCacheSize())
        self.querynumber = 0
        self.setupConnections()
        self.initLibraryTab()

    def setupConnections(self):
        QtCore.QObject.connect(self.searchDialog.searchButton, QtCore.SIGNAL("clicked()"), self.searchButtonClicked)
        QtCore.QObject.connect(self.searchDialog.leftTabWidget_Results, QtCore.SIGNAL("tabCloseRequested(int)"), self.closeTab)
        self.searchDialog.searchButton.setText("Search Lyrics Cache (%s)" % self.cachesize)

    def initLibraryTab(self):
        library = self.lyricsCacherRef.getLibraryDict()
        if library is None:
            return False
        newtab = QtGui.QWidget()
        verticallayout = QtGui.QVBoxLayout(newtab)
        treeWidget = QtGui.QTreeWidget(newtab)
        treeWidget.setHeaderLabel("Lyrics Cache")
        verticallayout.addWidget(treeWidget)
        self.searchDialog.leftTabWidget_Results.addTab(newtab, "Library (%s)" % self.cachesize)
        #Hide the tab's close button. We want this tab to be permanent.
        self.searchDialog.leftTabWidget_Results.tabBar().tabButton(0, QtGui.QTabBar.RightSide).resize(0,0)
        QtCore.QObject.connect(treeWidget, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*, int)"), self.treeItemClicked)
        artists = library.keys()
        artists.sort()
        for a in artists:
            artist_item = QtGui.QTreeWidgetItem(treeWidget)
            artist_item.setText(0, a)
            for song in library[a]:
                song_item = QtGui.QTreeWidgetItem(artist_item)
                song_item.setText(0, song)
                song_item.setData(0, QtCore.Qt.UserRole, library[a][song])

    def searchCountUpdate(self, n, total):
        self.searchDialog.searchButton.setText("Cancel Search  -  %s/%s" % (n, total))
        tabidx = self.searchDialog.leftTabWidget_Results.indexOf(self.activeSearchJobWidget)
        tabtext = unicode(self.searchDialog.leftTabWidget_Results.tabText(tabidx), "utf-8")
        endbracketidx = tabtext.index("]")
        listwidgetref = self.activeSearchJobWidget.findChild(QtGui.QListWidget, "resultsListWidget")
        self.searchDialog.leftTabWidget_Results.setTabText(tabidx, "[%s]" % str(listwidgetref.count()) + tabtext[endbracketidx+1:])


    def killActiveSearchThread(self):
        if self.searchThread is not None:
            self.searchJobTask.quitting = True
            self.searchThread.quit()
            self.searchThread.wait()
            if self.searchJobTask is not None:
                QtCore.QObject.disconnect(self.searchThread, QtCore.SIGNAL("started()"), self.searchJobTask.startSearch)
                QtCore.QObject.disconnect(self.searchJobTask, QtCore.SIGNAL("workFinished()"), self.searchThread.quit)
                QtCore.QObject.disconnect(self.searchJobTask, QtCore.SIGNAL("SearchFinished"), self.searchJobFinished)
                QtCore.QObject.disconnect(self.searchJobTask, QtCore.SIGNAL("SearchCountUpdate"), self.searchCountUpdate)
        self.activeSearchJobWidget = None
        QtCore.QObject.disconnect(self.searchDialog.searchButton, QtCore.SIGNAL("clicked()"), self.searchJobFinished)
        QtCore.QObject.connect(self.searchDialog.searchButton, QtCore.SIGNAL("clicked()"), self.searchButtonClicked)
        self.searchDialog.searchButton.setText("Search Lyrics Cache (%s)" % self.cachesize)
        self.setInputEnabledState(True)

    def searchJobFinished(self):
        self.killActiveSearchThread()
        #Update tab text with the number of search results.
        #No need to check if we have a tab to set to since we now always have a library tab
        curtabidx = self.searchDialog.leftTabWidget_Results.count()-1
        self.searchDialog.leftTabWidget_Results.setCurrentIndex(curtabidx)
        tabtext = unicode(self.searchDialog.leftTabWidget_Results.tabText(curtabidx)).encode("utf8")
        endbracketidx = tabtext.index("]")
        listwidgetref = self.searchDialog.leftTabWidget_Results.currentWidget().findChild(QtGui.QListWidget, "resultsListWidget")
        self.searchDialog.leftTabWidget_Results.setTabText(curtabidx, "[%s]" % str(listwidgetref.count()) + tabtext[endbracketidx+1:])

    def listItemClicked(self, listWidgetItem):
        self.searchDialog.resultLyricsView.setHtml(listWidgetItem.data(QtCore.Qt.UserRole).toPyObject())

    def treeItemClicked(self, treeWidgetItem, column):
        lyrics = treeWidgetItem.data(column, QtCore.Qt.UserRole).toPyObject()
        if isinstance(lyrics, QtCore.QString):
            self.searchDialog.resultLyricsView.setHtml(lyrics)

    def setInputEnabledState(self, state):
        self.searchDialog.songNameInput.setEnabled(state)
        self.searchDialog.artistNameInput.setEnabled(state)
        self.searchDialog.lyricsSearchStringInput.setEnabled(state)
        self.searchDialog.exactMatchCheckbox_Song.setEnabled(state)
        self.searchDialog.exactMatchCheckbox_Artist.setEnabled(state)
        self.searchDialog.exactMatchCheckbox_SearchString.setEnabled(state)

    def createSearchJob(self, pagereference):
        #Gather our search parameters
        searchparams = {}
        searchparams["song"] = self.searchDialog.songNameInput.text()
        searchparams["artist"] = self.searchDialog.artistNameInput.text()
        searchparams["searchString"] = self.searchDialog.lyricsSearchStringInput.text()
        searchparams["exactMatch_Song"] = self.searchDialog.exactMatchCheckbox_Song.isChecked()
        searchparams["exactMatch_Artist"] = self.searchDialog.exactMatchCheckbox_Artist.isChecked()
        searchparams["exactMatch_SearchString"] = self.searchDialog.exactMatchCheckbox_SearchString.isChecked()
        self.searchThread = QtCore.QThread()
        self.searchJobTask = searchJob(pagereference, searchparams, self.lyricsCacherRef)
        self.searchJobTask.moveToThread(self.searchThread)
        QtCore.QObject.connect(self.searchThread, QtCore.SIGNAL("started()"), self.searchJobTask.startSearch)
        QtCore.QObject.connect(self.searchJobTask, QtCore.SIGNAL("workFinished()"), self.searchThread.quit)
        QtCore.QObject.connect(self.searchJobTask, QtCore.SIGNAL("SearchFinished"), self.searchJobFinished)
        QtCore.QObject.connect(self.searchJobTask, QtCore.SIGNAL("SearchCountUpdate"), self.searchCountUpdate)
        self.searchThread.start()
        self.activeSearchJobWidget = pagereference
        #Swap our search button to a cancel button
        QtCore.QObject.disconnect(self.searchDialog.searchButton, QtCore.SIGNAL("clicked()"), self.searchButtonClicked)
        QtCore.QObject.connect(self.searchDialog.searchButton, QtCore.SIGNAL("clicked()"), self.searchJobFinished)
        self.searchDialog.searchButton.setText("Cancel Search  -  0/0")
        self.setInputEnabledState(False)


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
        self.querynumber += 1
        tabtitle = "[...] Search Query %s" % str(self.querynumber)
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
        self.killActiveSearchThread()