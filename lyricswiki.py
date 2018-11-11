# encoding: utf-8
#lyricswiki.py - by Kyle Claisse - 2013
#
#This script was designed specifically to pull lyrics from lyrics.wikia.com using their SOAP interface. This is a pretty poor lyrics provider so I added in a fallback 
#lyrics provider using songlyrics.com. Unfortunately songlyrics.com doesn't provide an API so we have to manually scrape the info ourselves using urllib
#
# Revision 014 
# Last Modified: April 21, 2016
#

import re, HTMLParser, urllib, urllib2, socket
from os import path
from os import sep as ossep
from suds.client import Client
from difflib import SequenceMatcher as sMatcher
from PyQt4 import QtCore
from lyrics_cacher import LyricsCacher

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

#This is the master probability value used to determine if a match has been found or not
#Anything over 0.6 is considered a good match but sometimes on titles that are very similar a higher ratio is required.
#This will be overridden by the user's options, this is just a fallback default.
_MASTER_RATIO = 0.65

#Turn debug mode on (True) or off (False) by changing this var, also manage the writing of extra debug info to disk.
_DEBUG_MODE = False
_DBGWRITE = False
_DBGWRITEFOLDER = path.dirname(path.realpath(__file__))


#Network timeout
socket.setdefaulttimeout(30)

#Just a quick little function to straighten out some of the escaped parenthesis before displaying them.
#Works on strings and tuples. Recurses only with tuples that have more than one backslash escaping the parenthesis (hasn't happened but it could).
def _pUnescape(ostring):
    fstring = "pUnescape Error"
    if isinstance(ostring, basestring):
        fstring = ostring
        while re.search("(\\\\[()])", fstring) is not None:
            fstring = fstring.replace("\)", ")")
            fstring = fstring.replace("\(", "(")
        
    if isinstance(ostring, tuple):
        fstring = ()
        for p in ostring:
            p = _pUnescape(p)
            fstring = fstring + (p,)
            
    return fstring



class lyricswikiObj(object):
    def __init__(self, context):
        self.context = context
        self.song = ""
        self.artist = ""
        self.Lyrics = ""
        self.searching = False
        self.last_return = [None, None]
        self.manual_mode = {"manual": False, "song": "", "artist": "", "song_at_set": "", "search_mode": False, "search_url": ""}
        self.songCache = LyricsCacher()

    def update_current_track(self, song, artist):
        self.song = song
        self.artist = artist

    def searchForLyrics(self, artist="", song=""):
        self.manual_mode["manual"] = True
        self.manual_mode["song_at_set"] = self.song
        #Only search when we have something to match for the song. No artist-only searches.
        if len(song) > 1:
            self.Lyrics = self._getLyrics(song, artist, search_mode=True)
        return self.Lyrics

    def resetManualEntry(self):
        self.manual_mode["manual"] = False
        self.manual_mode["search_mode"] = False
        self.manual_mode["song_at_set"] = ""
        self.manual_mode["song"] = ""
        self.manual_mode["url"] = ""
        self.manual_mode["artist"] = ""

    def manual_url_set(self, url):
        url_split = re.split("::", url)
        #url_split[0] = url
        #url_split[1] = song title
        #url_split[2] = artist
        self.has_searched = False
        self.manual_mode["manual"] = True
        self.manual_mode["search_mode"] = True
        self.manual_mode["artist"] = url_split[2]
        self.manual_mode["song"] = url_split[1]
        self.manual_mode["search_url"] = url_split[0]
        #self.update_current_track(self.manual_mode["song"], self.manual_mode["artist"])
        if self.song is None:
            self.song = ""
        self.manual_mode["song_at_set"] = self.song
        self.song = self.manual_mode["song"]
        self.artist = self.manual_mode["artist"]
        self.Lyrics = self.getLyrics()

    def manual_song_set(self, song_artist):
        if song_artist[0] and song_artist[1]:
            print "Querying artist and song manually..."
            self.manual_mode["manual"] = True
            self.manual_mode["artist"] = song_artist[0]
            self.manual_mode["song"] = song_artist[1]
            self.update_current_track(self.manual_mode["song"], self.manual_mode["artist"])
            if self.song is None:
                self.song = ""
            self.manual_mode["song_at_set"] = self.song

    def getLyrics(self):
        if self.manual_mode["manual"] is True:
            if self.manual_mode["song_at_set"] != self.context.actual_song:
                self.manual_mode["manual"] = False
            if self.manual_mode["search_mode"] is False:
                return None

        if self.manual_mode["search_mode"] is True:
            #We clicked on a result
            print "2"
        if self.context.hasSongChanged() is True:
        #Check if we have this song cached
            if self.songCache.checkSong(self.song, self.artist) is True:
                cachedlyrics = self.songCache.getLyrics(self.song, self.artist)
                if len(cachedlyrics) > 0:
                    print "Returned cached lyrics for '%s' by %s" % (self.song, self.artist)
                    return cachedlyrics
                else:
                    print "Zero length lyrics cache file, trying to grab fresh lyrics..."
            #We either dont have it cached or the cached lyrics were empty
            self.Lyrics = self._getLyrics(self.song, self.artist, manual_mode=self.manual_mode["manual"])
            try:
                self.Lyrics = self.Lyrics.encode("utf8")
            except:
                pass
            self.last_return = [self.song, self.artist]
            self.songCache.saveLyrics(self.song, self.artist, self.Lyrics)
            return self.Lyrics
        else:
            return None

    @staticmethod
    def setInternalOptions(options):
        global _MASTER_RATIO, _DBGWRITE, _DEBUG_MODE, _DBGWRITEFOLDER
        #Set the options
        _MASTER_RATIO = float(options["masterMatchRatio"])
        _DBGWRITE = options["debugWriteEnabled"]
        _DEBUG_MODE = options["debugModeEnabled"]
        _DBGWRITEFOLDER = options["debugOutputFolder"]

    #Yeah thats ugly, tacking on a _ onto the beginning.... Fite me...
    def _getLyrics(self, song, artist, manual_mode=False, search_mode=False, search_url=None):
        if search_mode is True:
            search_results = self.songlyrics_getLyrics(song, artist, search_mode=True)
            return search_results
        
        if search_url is not None:
            self._DEBUG("mainGL: Getting lyrics for supplied url")
            songLyrics = self.songlyrics_getLyrics(song, artist, url=search_url)
            return songLyrics

        #We'll try both the wikia and songlyrics.com functions before we give up
        self._DEBUG("mainGL: Getting lyrics from wikia_getLyrics()")
        try:
            songLyrics = self.wikia_getLyrics(song, artist)
            #songLyrics = None
        except Exception as e:
            songLyrics = None
            """
            print "Wikia failed with following error:"
            print e
            """
        #songLyrics = None
        if songLyrics is None:
            self._DEBUG("mainGL: Previous function returned None, getting lyrics from songlyrics_getLyrics()")
            songLyrics = self.songlyrics_getLyrics(song, artist)
        
        #Now we test the length of the lyrics returned, setting the lyrics as "Lyrics not found" if required.
        if len(songLyrics) < 2:
            self._DEBUG("mainGL: Lyrics were too short, changing to 'not found'")
            songLyrics = "Sorry, the lyrics were not found.  :("
        
        return songLyrics
    

    def wikia_getLyrics(self, song, artist):
        self._DEBUG("lwoGlDBG 1: START")
        #Check if we've been given an empty song or artist
        if artist is None or song is None:
            print "A0 DBG: Artist or Song is None, errors will ensue..."
        if len(artist.strip()) < 1 or len(song.strip()) < 1:
            print "A0 DBG: Artist or Song is an empty string, errors will ensue..."
        
        url = "http://lyrics.wikia.com/server.php?wsdl"
        cli = Client(url)
        lurl = cli.service.getSong(_pUnescape(artist), _pUnescape(song)).url
        if len(lurl) > 0: self._DEBUG("lwoGlDBG lurl: " + str(lurl))
        #If the url contains the suffix 'edit' somewhere we know there are no lyrics for this song.
        if re.match("^(.*)action=edit$", lurl) is not None:
            self._DEBUG("lwoGlDBG 2: EDIT FOUND, GO ALT")
            return None
        #Now we open the URL and return the html
        self._DEBUG("lwoGlDBG 3: Creating URL opener")
        urlOpener = urllib.urlopen(lurl)
        self._DEBUG("lwoGlDBG 4: Reading html")
        html = urlOpener.read()
        urlOpener.close()
        self._DEBUG(html, write=True, filen="lwoGlDBG_html-%s_%s.txt" % (song, artist))
        #Test if its been encoded or not
        fcrap = None
        try:
            self._DEBUG("lwoGlDBG-t1 a")
            fcrap = re.search("class='lyricbox'>(.*);<!--", html).group(1)
            self._DEBUG("lwoGlDBG-t1 b")
            cleancrap = re.search("((?:</[a-zA-Z]{1,15}>){0,6})&#(.*)", fcrap)
            self._DEBUG("lwoGlDBG-t1 c")
            encoded = True
        except:
            #Try second guess
            try:
                self._DEBUG("lwoGlDBG-t1 e")
                fcrap = re.search("class='lyricbox'>(.*)<div class='lyricsbreak'></div>", html).group(1)
                self._DEBUG("lwoGlDBG-t1 f")
                cleancrap = re.search("((?:</[a-zA-Z]{1,15}>){0,6})&#(.*)", fcrap)
                self._DEBUG("lwoGlDBG-t1 g")
                encoded = True
            except:    
                #Ok so its not escaped, just in plaintext
                self._DEBUG("lwoGlDBG-t1 d")
                encoded = False
        
        if encoded:
            self._DEBUG(fcrap, write=True, filen="fcrap-%s_%s.txt" % (song, artist))
            self._DEBUG("lwoGlDBG cleancrap: " + str(cleancrap))
            self._DEBUG("lwoGlDBG-e1 a")
            hparse = HTMLParser.HTMLParser()
            if cleancrap is None:
                self._DEBUG("lwoGlDBG GOING ALT 1")
                return None
    
            if cleancrap.group(1) is not None:
                actual = cleancrap.group(1) + "&#" + str(cleancrap.group(2))
            else:        
                actual = "&#" + str(cleancrap.group(2)) #Just putting back some characters that were cut earlier in processing
            if actual[-1] != ";":
                actual += ";"
            almostdone = hparse.unescape(actual)
            finishedlyrics = almostdone
            #finishedlyrics = almostdone.replace("<br />", "\n")
            #finishedlyrics = finishedlyrics.replace("<br>", "\n")
        else:
            self._DEBUG("lwoGlDBG-ne1 START")
            try:
                self._DEBUG("lwoGlDBG-ne1 a")
                fcrap = re.search('class="lyricbox">(.*)', html)
                print "a1 dbg, fcrap:", fcrap
                crap2 = re.search('alt="phone" width="16" height="17">(.*)', fcrap.group(1))
                self._DEBUG("lwoGlDBG-ne1 b")
                cleancrap = re.search("</a></div>(.*)", crap2.group(1))
                self._DEBUG("lwoGlDBG-ne1 c")
                finishedlyrics = cleancrap.group(1)
                #finishedlyrics = cleancrap.group(1).replace("<br />", "\n")
                #finishedlyrics = finishedlyrics.replace("<br>", "\n")
                self._DEBUG("lwoGlDBG-ne1 d")
            except:
                self._DEBUG("lwoGlDBG GOING ALT 2")
                return None
                
        #Ok now we check to see if these lyrics are complete or if we are getting just the first part and the rest is missing
        #Returned lyrics with this problem usually have an error message appended to them so we can check for that.
        
        if re.search("Unfortunately(.*?)not licensed(.*?)random page", finishedlyrics) is not None:    #This is kind of a weak regular expression and it could easily change format in the future
            self._DEBUG("lwoGlDBG GOING ALT 3")
            finishedlyrics = self.songlyrics_getLyrics(song, artist)
    
        else:
            print "DEBUG_LURL: " + str(lurl)
            
        return finishedlyrics
    
    
    
    def songlyrics_getLyrics(self, song, artist, search_mode=False, url=None):
        hparse = HTMLParser.HTMLParser()
        
        #Ok this other website doesn't offer us an easy-to-use API so we have to manually scrape their website and figure it out ourselves
        #We are going to first search using the format: "Artist - Song Title" and we'll just take whatever comes back first in the results.
        #This might need to be refined in the future if it fails to accurately return lyrics
        
        #This is our base url for searching on songlyrics
        surl = "http://www.songlyrics.com/index.php?section=search&searchW=%s"
        
        #First thing we are going to do is whip up a proper url with our search query in it
        quotestr = _pUnescape(artist) + " " + _pUnescape(song)
        query_data = urllib.quote_plus(quotestr)
        queryurl = surl % query_data
        
        #Now lets execute the search and get the html returned so we can work on it
        downloaderHeaders = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "deflate",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
        }
        
        try:
            request = urllib2.Request(queryurl, None, downloaderHeaders)
            search_query = urllib2.urlopen(request)
            search_html = search_query.read()
            search_query.close()
        except:
            return "A connection error has occurred."
    
        #Some stuff needs the song/artist name to be clean
        clean_song = _pUnescape(song)
        clean_artist = _pUnescape(artist)
        if search_mode is True:
            search_results = self.songlyrics_getLyricsURL(song, artist, search_html, search_mode=True)
            return search_results
        
        
        
        self._DEBUG("-------------------")
        self._DEBUG("SONG: " + clean_song)
        self._DEBUG("ARTIST: " + clean_artist)
        self._DEBUG("-------------------")
        self._DEBUG("QUERY_DATA: " + query_data)
        self._DEBUG("QUERY URL: " + queryurl)
        self._DEBUG("-------------------")
        
        self._DEBUG(search_html, True, "raw_search_html-%s.html" % clean_song)
        if url is None:
            #Now we need to find the url for the right song in this mess of HTML
            #Lucky for us the title of each song is listed in an href tag and makes the job much easier
            try:
                self._DEBUG("lwDBG A"); lwdbgstage = "A"
                #The initial lyrics results start just under the div labeled 'search-results' and ends just before the last ul tag labeled 'pagination'
                refined_results = re.search("<div class=\"search-results\">(.*)<ul class=\"pagination\">", search_html, re.S|re.I).group(1)
                
                self._DEBUG("lwDBG B"); lwdbgstage = "B"
                
                self._DEBUG(refined_results, True, "refined_results-%s.html" % clean_song)
                #And now we look for the title of our song in the results. This is where it will fail most of the time. We need to find a different way to search the song name without being so rigid.
                refined_results = re.search("title=\"%s\"(.*?)<div class=\"serpresult\">" % song, refined_results, re.S|re.I).group(1)
                
                self._DEBUG("lwDBG C"); lwdbgstage = "C"
                #And finally we extract the url to the lyrics from the refined results
                lyrics_url = re.search("<a href=\"(.*?)\" title=\"%s\">%s lyrics" % (song, song), refined_results, re.S|re.I).group(1)
                
                self._DEBUG("lwDBG D"); lwdbgstage = "D"
            except Exception as e:
                #We now make one attempt to match up the song title with the first few results using difflib unless the user wants the results for a search
                lyrics_url = self.songlyrics_getLyricsURL(song, artist, refined_results)
                if lyrics_url is None:
                    #If at any time something after here fails we return the error and don't even attempt to continue
                    print "a4 lwDBG_STAGE: " + lwdbgstage + " -- qURL: " + str(queryurl)
                    return "No lyrics for this song or something else went wrong, sorry.  :(<br><br>Song: %s<br>Artist: %s<br><br>Search URL: %s" % (clean_song, clean_artist, queryurl)
            
        else:
            lyrics_url = url
        
        self._DEBUG("LYRICS_URL: " + lyrics_url)
        
    
        # OK, if we've gotten this far we should have a lyrics_url with the proper url inside it. Now all we have to
        # do is download the page lyrics_url is pointing to and cut out just the lyrics
        lyrics_request = urllib2.Request(lyrics_url, None, downloaderHeaders)
        lyrics_query = urllib2.urlopen(lyrics_request)
        lyrics_html = lyrics_query.read()
        lyrics_query.close()
        
        self._DEBUG(lyrics_html, True, "raw_lyrics_html-%s.html" % clean_song)
        
        #Now we cut out just the lyrics, unfortunately they appaeared to be garbled just like lyricswiki does to their songs
        #This is easy enough to fix ofc using HTMLParser
        
        lyrics_raw = re.search("id=\"songLyricsDiv\"(.*?)>(.*?)</p>", lyrics_html, re.S|re.I).group(2)
        
        #Before we do any unescaping we need to replace any nasty characters. This is incomplete for now but it works and will be updated as new problem characters are found.
        lyrics_raw = self.sanitize(lyrics_raw)
        
        #First we have to cut out the header this site adds into their lyrics, its just the first three lines so nothing too difficult
        #We're only going to do this if the first three lines are what we think they are. The first line is usually the artist if it's there.
        lyrics_split = lyrics_raw.split("<br />")
        if hparse.unescape(lyrics_split[0]) == artist:
            lyrics_only = lyrics_split[3:]
            final_lyrics = "<br />".join(lyrics_only)
        
        else:
            #We dont have that header so we dont do anything
            final_lyrics = lyrics_raw
        #And now we decode and unescape the string back into plain english and we're DONE!
        final_lyrics = hparse.unescape(final_lyrics.decode("ascii", "ignore")) #The decode should remove anything the above replacement code didnt get
        
        
        print "DEBUG_LURL: " + str(lyrics_url)
        self._DEBUG("=======END SEQUENCE ALT LYRICS=======")
        return final_lyrics
        
    def songlyrics_getLyricsURL(self, song, artist, html, search_mode=False):
        self._DEBUG("ALT_GET_LYRICS_URL")
        #Before we do anything we need to make sure no weird chars are in it
        html = self.sanitize(html)
        cleansong = song.replace("'", "")
        cleansong = cleansong.replace('"', '')
        #cleansong = re.search("(.*)\s+[([{]", cleansong).group(1)
        #First thing we do is separate out each result and then check each one to see if the title matches or not
        split_results = re.split('<div class="serpresult">', html)
        
        #search mode stuffs
        search_mode_results = []
        
        #We'll loop through each item and separate out the link title from each one. Then we'll compare the title with our song title and see if they match.
        self._DEBUG("agluDBG A")
        for entry in split_results:
            self._DEBUG("agluDBG B")
            if re.search("serpdesc-2", entry, re.I) is not None: #make sure this is a lyrics entry and not garbage
                self._DEBUG("agluDBG C")
                if search_mode is True:
                    tmpdata = {}
                    #We need to separate out three parts, the song title, the artist, and the url.
                    tmpdata["url"], tmpdata["title"] = re.search("<h3><a href=\"(.*?)\" title=\"(.*?)\">", entry, re.S|re.I).groups()
                    tmpdata["artist"] = re.search('''by <a href="(?:.*?)">(.*?)</a>''', entry, re.I).group(1)
                    search_mode_results.append(tmpdata)
                    continue
                #Now we pull out the title as it is on the page
                entry_url, entry_title = re.search("<h3><a href=\"(.*?)\" title=\"(.*?)\">", entry, re.S|re.I).groups() #Slick way to set both vars at once with only one re.search()
                #now we test the entry title we pulled out against our song title and see if they are close enough match. If so, we return the url, if not we modify our title slighty and try again
                if sMatcher(None, song, entry_title).ratio() > _MASTER_RATIO:
                    if sMatcher(None, artist, re.search('''by <a href="(?:.*?)">(.*?)</a>''', entry, re.I).group(1)).ratio() > _MASTER_RATIO: #Verify artist is correct too
                        self._DEBUG("a5 P0")
                        return entry_url
                #ok so now we just cut anything off the end of the song and artist that's in parenthesis, brackets, or braces () [] and {}
                #We also remove any quotes, single or double as well as turn up the _MASTER_RATIO by .1 to compensate for the removal of crap. Trust me, it works.
                #Then we retest againt the _MASTER_RATIO and see if it fits now. If not again we forget about it (this could be bad when trying to differentiate between two songs that only differ by their end)
                elif re.search("(.*?) ?[([{]", cleansong) is not None and sMatcher(None, re.search("(.*?) ?[([{]", cleansong, re.S|re.I).group(1), entry_title).ratio() > _MASTER_RATIO+0.1:
                    self._DEBUG("agluDBG D")
                    if sMatcher(None, artist, re.search('''by <a href="(?:.*?)">(.*?)</a>''', entry, re.I).group(1)).ratio() > _MASTER_RATIO:
                        self._DEBUG("a5 P1")
                        return entry_url
                    elif re.search("(.*?) ?[([{]", artist) is not None and sMatcher(None, re.search("(.*?) ?[([{]", artist).group(1), re.search('''by <a href="(?:.*?)">(.*?)</a>''', entry, re.I).group(1)).ratio() > _MASTER_RATIO:
                        self._DEBUG("a5 P2")
                        return entry_url
                elif re.search("(.*?) ?[([{]", artist) is not None and sMatcher(None, re.search("(.*?) ?[([{]", artist).group(1), re.search('''by <a href="(?:.*?)">(.*?)</a>''', entry, re.I).group(1)).ratio() > _MASTER_RATIO:
                    self._DEBUG("agluDBG E")
                    if sMatcher(None, cleansong, entry_title).ratio() > _MASTER_RATIO:
                        self._DEBUG("a5 P3")
                        return entry_url
        if search_mode is True:
            return search_mode_results
        
        self._DEBUG("a5 P4")
        return None
    
    @staticmethod
    def sanitize(input_text):
        '''This function replaces certain non-ascii characters with workable ascii counterparts'''
        if isinstance(input_text, str):
            input_text = input_text.replace("\xe2\x80\x99", "'")  #RIGHT SINGLE QUOTATION MARK
            input_text = input_text.replace("\xe2\x80\x98", "'")  #LEFT SINGLE QUOTATION MARK
            input_text = input_text.replace("\xe2\x80\x9c", "\"") #LEFT DOUBLE QUOTATION MARK
            input_text = input_text.replace("\xe2\x80\x9d", "\"") #RIGHT DOUBLE QUOTATION MARK
            input_text = input_text.replace("\xe2\x80\xa6", "...")#HORIZONTAL ELLIPSIS (three dots: ...)
            input_text = input_text.replace("\xc2\xbf", "?")      #INVERTED QUESTION MARK
            input_text = input_text.replace("\xc2\xa1", "!")      #INVERTED EXCLAMATION MARK
        else:
            raise TypeError("Input object to sanitize() is not an instance of str") #There's really no need to raise an exception here since we handle errors the same way we handle normal output text.
        
        return input_text


    @staticmethod
    def _DEBUG(msg, write=False, filen=None):
        if _DEBUG_MODE:
            if write:
                if _DBGWRITE:
                    #clean up the filename
                    filen = filen.replace("\\", "-")
                    filen = filen.replace("/", "-")
                    filen = filen.replace(":", "-")
                    filen = filen.replace("*", "+")
                    filen = filen.replace("?", "")
                    filen = filen.replace("\"", "'")
                    filen = filen.replace("<", "[")
                    filen = filen.replace(">", "]")
                    filen = filen.replace("|", "-")
                    fullfilepath = _DBGWRITEFOLDER + ossep + filen
                    r = open(fullfilepath, 'a')
                    r.write(msg)
                    r.close()
                    print "DEBUG_WRITE"
            else:
                print msg
                