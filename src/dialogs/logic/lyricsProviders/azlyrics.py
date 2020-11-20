from urllib import quote_plus
import re
from difflib import SequenceMatcher as sMatcher
from .seleniumDriver import getHtmlWithDriver

LYRICS_PROVIDER_NAME="AZlyrics"
LYRICS_PROVIDER_VERSION="1.2"
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
        query_data = quote_plus(song + " " + artist)
        queryurl = surl % query_data

        #Having to use Selenium now since even AZlyrics has started to block normal requests with special CSS.
        #Wonder how long until they start detecting Selenium...
        search_html = getHtmlWithDriver(queryurl)

        search_results = re.search("^.*Song results.*?<td class=\"text-left visitedlyr\".*?>(.*?)(?:</table>).*</html>$", search_html.strip(), re.S|re.MULTILINE)
        if search_results is not None:
            split_results = re.split("<td class=\"text-left visitedlyr\".*?>", search_results.group(1))
            for idx, result in enumerate(split_results):
                result_url, result_songartist = re.search("%s\..*?<a href=\"(.*?)\">((?:.*?)-(?:.*))" % str(idx+1), result).groups()
                result_song, result_artist = re.search("<b>\"(.*?)\"</b>\s+</a>\s+-\s+<b>(.*?)</b>", result_songartist).groups()

                #Check if this result is the right one
                if sMatcher(None, song.lower(), result_song.lower()).ratio() > self._MASTER_RATIO and sMatcher(None, artist.lower(), result_artist.lower()).ratio() > self._MASTER_RATIO:
                    #Time to get the lyrics
                    lyrics_html = getHtmlWithDriver(result_url)

                    #We're not a third party lyrics provider rite??? Psshhhhh
                    warnbanner = "<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->"
                    return re.search("<div>.*?%s(.*?)</div>" % warnbanner, lyrics_html, re.S|re.I).group(1).strip()
        return None
