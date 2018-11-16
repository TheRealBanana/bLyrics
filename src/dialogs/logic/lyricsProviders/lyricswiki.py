import re, HTMLParser, urllib
from suds.client import Client
from PyQt4 import QtCore



LYRICS_PROVIDER_NAME="Lyricswiki"
LYRICS_PROVIDER_VERSION="1.1"
#Lyrics provider priority allows bLyrics to order lyrics providers properly. Lower numbered providers will be used
#before higher numbered providers. Put the really slow ones at the end if you want cache generation to be quick.
#Otherwise make the most reliable (in terms of lyrical content) the first priority. Providers with the same priority
#are not guaranteed to run in any specific order.
LYRICS_PROVIDER_PRIORITY=0


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

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

    def getLyrics(self, song, artist):
        url = "http://lyrics.wikia.com/server.php?wsdl"
        cli = Client(url)
        try:
            lurl = cli.service.getSong(_pUnescape(artist), _pUnescape(song)).url
        except:
            return None
        #If the url contains the suffix 'edit' somewhere we know there are no lyrics for this song.
        if re.match("^(.*)action=edit$", lurl) is not None:
            return None
        #Now we open the URL and return the html
        urlOpener = urllib.urlopen(lurl)
        html = urlOpener.read()
        urlOpener.close()
        #Test if its been encoded or not
        try:
            fcrap = re.search("class='lyricbox'>(.*);<!--", html).group(1)
            cleancrap = re.search("((?:</[a-zA-Z]{1,15}>){0,6})&#(.*)", fcrap)
            encoded = True
        except:
            #Try second guess
            try:
                fcrap = re.search("class='lyricbox'>(.*)<div class='lyricsbreak'></div>", html).group(1)
                cleancrap = re.search("((?:</[a-zA-Z]{1,15}>){0,6})&#(.*)", fcrap)
                encoded = True
            except:    
                #Ok so its not escaped, just in plaintext
                encoded = False
        if encoded:
            hparse = HTMLParser.HTMLParser()
            if cleancrap is None:
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
            try:
                fcrap = re.search('class="lyricbox">(.*)', html)
                crap2 = re.search('alt="phone" width="16" height="17">(.*)', fcrap.group(1))
                cleancrap = re.search("</a></div>(.*)", crap2.group(1))
                finishedlyrics = cleancrap.group(1)
                #finishedlyrics = cleancrap.group(1).replace("<br />", "\n")
                #finishedlyrics = finishedlyrics.replace("<br>", "\n")
            except:
                return None
        #Ok now we check to see if these lyrics are complete or if we are getting just the first part and the rest is missing
        #Returned lyrics with this problem usually have an error message appended to them so we can check for that.
        if re.search("Unfortunately(.*?)not licensed(.*?)random page", finishedlyrics) is not None:    #This is kind of a weak regular expression and it could easily change format in the future
            return None
        else:
            pass
            #print "DEBUG_LURL: " + str(lurl)
        #Instrumentals
        if re.search("<b>Instrumental</b>", finishedlyrics) is not None:
            finishedlyrics = "<b>Instrumental</b>"
        return finishedlyrics
    
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