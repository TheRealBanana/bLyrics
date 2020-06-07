import urllib
import urllib2
import re
from difflib import SequenceMatcher as sMatcher

LYRICS_PROVIDER_NAME="AZlyrics"
LYRICS_PROVIDER_VERSION="1.1"
#Lyrics provider priority allows bLyrics to order lyrics providers properly. Lower numbered providers will be used
#before higher numbered providers. Put the really slow ones at the end if you want cache generation to be quick.
#Otherwise make the most reliable (in terms of lyrical content) the first priority. Providers with the same priority
#are not guaranteed to run in any specific order.
LYRICS_PROVIDER_PRIORITY=0

class LyricsProvider(object):
    def __init__(self, MASTER_RATIO=0.65):
        self._MASTER_RATIO = MASTER_RATIO
        self.LYRICS_PROVIDER_NAME = LYRICS_PROVIDER_NAME
        self.LYRICS_PROVIDER_VERSION = LYRICS_PROVIDER_VERSION

    def getLyrics(self, song, artist):
        surl = "https://search.azlyrics.com/search.php?q=%s&w=songs&p=1"
        query_data = urllib.quote_plus(song + " " + artist)
        queryurl = surl % query_data

        #Now lets execute the search and get the html returned so we can work on it
        downloaderHeaders = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "deflate",
            "DNT": "1",
            "Connection": "keep-alive",
        }

        try:
            request = urllib2.Request(queryurl, None, downloaderHeaders)
            search_query = urllib2.urlopen(request)
            search_html = search_query.read()
            search_query.close()
        except:
            return None

        search_results = re.search("^.*Song results.*?<td class=\"text-left visitedlyr\".*?>(.*?)(?:</table>).*</html>$", search_html.strip(), re.S|re.MULTILINE)
        if search_results is not None:
            split_results = re.split("<td class=\"text-left visitedlyr\".*?>", search_results.group(1))
            for idx, result in enumerate(split_results):
                result_url, result_songartist = re.search("%s\..*?<a href=\"(.*?)\">((?:.*?)-(?:.*))" % str(idx+1), result).groups()
                result_song, result_artist = re.search("<b>\"(.*?)\"</b>\s+</a>\s+-\s+<b>(.*?)</b><br>", result_songartist).groups()

                #Check if this result is the right one
                if sMatcher(None, song.lower(), result_song.lower()).ratio() > self._MASTER_RATIO and sMatcher(None, artist.lower(), result_artist.lower()).ratio() > self._MASTER_RATIO:
                    #Time to get the lyrics
                    lyrics_request = urllib2.Request(result_url, None, downloaderHeaders)
                    lyrics_query = urllib2.urlopen(lyrics_request)
                    lyrics_html = lyrics_query.read()
                    lyrics_query.close()
                    #We're not a third party lyrics provider rite??? Psshhhhh
                    warnbanner = "<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->"
                    return re.search("<div>.*?%s(.*?)</div>" % warnbanner, lyrics_html, re.S|re.I).group(1).strip()
        return None
