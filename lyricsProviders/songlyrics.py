import re, HTMLParser, urllib, urllib2
from difflib import SequenceMatcher as sMatcher
from PyQt4 import QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s



LYRICS_PROVIDER_NAME="Songlyrics"
LYRICS_PROVIDER_VERSION="1.1"



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



class LyricsProvider(object):
    def __init__(self, MASTER_RATIO=0.65):
        self._MASTER_RATIO = MASTER_RATIO
        self.LYRICS_PROVIDER_NAME = LYRICS_PROVIDER_NAME
        self.LYRICS_PROVIDER_VERSION = LYRICS_PROVIDER_VERSION

    def getLyrics(self, song, artist, search_mode=False, url=None):
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

        if url is None:
            #Now we need to find the url for the right song in this mess of HTML
            #Lucky for us the title of each song is listed in an href tag and makes the job much easier
            try:
                #The initial lyrics results start just under the div labeled 'search-results' and ends just before the last ul tag labeled 'pagination'
                refined_results = re.search("<div class=\"search-results\">(.*)<ul class=\"pagination\">", search_html, re.S|re.I).group(1)
                #And now we look for the title of our song in the results. This is where it will fail most of the time. We need to find a different way to search the song name without being so rigid.
                refined_results = re.search("title=\"%s\"(.*?)<div class=\"serpresult\">" % song, refined_results, re.S|re.I).group(1)
                #And finally we extract the url to the lyrics from the refined results
                lyrics_url = re.search("<a href=\"(.*?)\" title=\"%s\">%s lyrics" % (song, song), refined_results, re.S|re.I).group(1)
            except Exception as e:
                #We now make one attempt to match up the song title with the first few results using difflib unless the user wants the results for a search
                lyrics_url = self.songlyrics_getLyricsURL(song, artist, refined_results)
                if lyrics_url is None:
                    #If at any time something after here fails we return the error and don't even attempt to continue
                    return "No lyrics for this song or something else went wrong, sorry.  :(<br><br>Song: %s<br>Artist: %s<br><br>Search URL: %s" % (clean_song, clean_artist, queryurl)
            
        else:
            lyrics_url = url
        
        # OK, if we've gotten this far we should have a lyrics_url with the proper url inside it. Now all we have to
        # do is download the page lyrics_url is pointing to and cut out just the lyrics
        lyrics_request = urllib2.Request(lyrics_url, None, downloaderHeaders)
        lyrics_query = urllib2.urlopen(lyrics_request)
        lyrics_html = lyrics_query.read()
        lyrics_query.close()
        
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

        if "We do not have the lyrics for" in final_lyrics:
            return None
        print "DEBUG_LURL: " + str(lyrics_url)
        return final_lyrics
        
    def songlyrics_getLyricsURL(self, song, artist, html, search_mode=False):
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
        for entry in split_results:
            if re.search("serpdesc-2", entry, re.I) is not None: #make sure this is a lyrics entry and not garbage
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
                if sMatcher(None, song, entry_title).ratio() > self._MASTER_RATIO:
                    if sMatcher(None, artist, re.search('''by <a href="(?:.*?)">(.*?)</a>''', entry, re.I).group(1)).ratio() > self._MASTER_RATIO: #Verify artist is correct too                        
                        return entry_url
                #ok so now we just cut anything off the end of the song and artist that's in parenthesis, brackets, or braces () [] and {}
                #We also remove any quotes, single or double as well as turn up the self._MASTER_RATIO by .1 to compensate for the removal of crap. Trust me, it works.
                #Then we retest againt the self._MASTER_RATIO and see if it fits now. If not again we forget about it (this could be bad when trying to differentiate between two songs that only differ by their end)
                elif re.search("(.*?) ?[([{]", cleansong) is not None and sMatcher(None, re.search("(.*?) ?[([{]", cleansong, re.S|re.I).group(1), entry_title).ratio() > self._MASTER_RATIO+0.1:                    
                    if sMatcher(None, artist, re.search('''by <a href="(?:.*?)">(.*?)</a>''', entry, re.I).group(1)).ratio() > self._MASTER_RATIO:                        
                        return entry_url
                    elif re.search("(.*?) ?[([{]", artist) is not None and sMatcher(None, re.search("(.*?) ?[([{]", artist).group(1), re.search('''by <a href="(?:.*?)">(.*?)</a>''', entry, re.I).group(1)).ratio() > self._MASTER_RATIO:                        
                        return entry_url
                elif re.search("(.*?) ?[([{]", artist) is not None and sMatcher(None, re.search("(.*?) ?[([{]", artist).group(1), re.search('''by <a href="(?:.*?)">(.*?)</a>''', entry, re.I).group(1)).ratio() > self._MASTER_RATIO:                    
                    if sMatcher(None, cleansong, entry_title).ratio() > self._MASTER_RATIO:
                        return entry_url
        if search_mode is True:
            return search_mode_results


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
                