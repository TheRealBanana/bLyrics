#So Genius.com requires an OAuth token to use their official API and I aint doin that
#This has to work for absolutely anyone who downloads this app, no tokens required.

import urllib
import urllib2
import json
import re
from difflib import SequenceMatcher as sMatcher
from HTMLParser import HTMLParser


LYRICS_PROVIDER_NAME="Genius"
LYRICS_PROVIDER_VERSION="1.0"
#Lyrics provider priority allows bLyrics to order lyrics providers properly. Lower numbered providers will be used
#before higher numbered providers. Put the really slow ones at the end if you want cache generation to be quick.
#Otherwise make the most reliable (in terms of lyrical content) the first priority. Providers with the same priority
#are not guaranteed to run in any specific order.
LYRICS_PROVIDER_PRIORITY=2



#Genius lyrics are highly obfuscated with HTML all over the place. Didn't want to use BeautifulSoup for this.
#Thankfully I found a great snippet on stackoverflow that does just what I need
# https://stackoverflow.com/a/925630
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


class LyricsProvider(object):
    def __init__(self, MASTER_RATIO=0.65):
        self._MASTER_RATIO = MASTER_RATIO
        self.LYRICS_PROVIDER_NAME = LYRICS_PROVIDER_NAME
        self.LYRICS_PROVIDER_VERSION = LYRICS_PROVIDER_VERSION

    def getLyrics(self, song, artist):
        final_lyrics = None
        surl = "https://genius.com/api/search/multi?page=1&q=%s"
        query_data = urllib.quote_plus(song + " " + artist)
        queryurl = surl % query_data

        #Now lets execute the search and get the html returned so we can work on it
        downloaderHeaders = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
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
        loaded_json = json.loads(search_html)
        #Didnt get error 401'd or 500'd so lets keep goin
        if loaded_json["meta"]["status"] == 200:
            results = loaded_json["response"]["sections"][0]["hits"]
            for r in results:
                resultdata = r["result"]
                #Some songs come back instrumental when they arent, dunno why
                #if resultdata["instrumental"] is True:
                #    return "<b>Instrumental</b>"
                result_url = resultdata["url"]
                result_song = resultdata["title"]
                result_artist = resultdata["primary_artist"]["name"]
                if sMatcher(None, song.lower(), result_song.lower()).ratio() > self._MASTER_RATIO and sMatcher(None, artist.lower(), result_artist.lower()).ratio() > self._MASTER_RATIO:
                    #Got good lyrics, lets get them
                    lyrics_request = urllib2.Request(result_url, None, downloaderHeaders)
                    lyrics_query = urllib2.urlopen(lyrics_request)
                    lyrics_html = lyrics_query.read()
                    lyrics_query.close()
                    raw_lyrics =  re.search("<div class=\"lyrics\">.*?<!--sse-->(.*?)<!--/sse-->", lyrics_html, re.S|re.I).group(1).strip()
                    stripper = MLStripper()
                    stripper.feed(raw_lyrics)
                    final_lyrics = stripper.get_data().strip().replace("\n", "<br>")
        return final_lyrics