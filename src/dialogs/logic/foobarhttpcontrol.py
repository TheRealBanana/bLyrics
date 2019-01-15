import urllib2
import json
from ast import literal_eval
import re
from HTMLParser import HTMLParser

#Downloads the current song/artist/playmode from foobar's ajquery web interface
class foobarStatusDownloader(object):
    def __init__(self, MWref, hostnameandport):
        self.MWref = MWref
        self.address = hostnameandport[0]
        self.port = hostnameandport[1]

    def queryWebInterface(self, urlsuffix="/ajquery/?param3=js/state.json", noreturn=False):
        try:
            page = urllib2.urlopen("http://" + str(self.address) + ":" + str(self.port) + str(urlsuffix))
            if noreturn:
                return None
            rawjson = page.read()
            page.close()
            try:
                data = json.loads(rawjson)
            except ValueError:
                #Was getting errors trying to load a 12k song playlist using json.loads()
                #I am acutely aware of how stupid evaling is, but this is the only mitigation I can find right now.
                #I will attempt to find a different workaround for this but for now we'll try and be as safe as we can.
                #NOT A GOOD IDEA WHY DO THIS?!
                data = literal_eval(rawjson)
                if isinstance(data, dict) is False:
                    return None
        except:
            return None
        return data


    def getStatus(self):
        data = self.queryWebInterface()

        if data is None:
            print "Connection error of some sort"
            return None

        isplaying = int(data["isPlaying"])
        ispaused = int(data["isPaused"])
        playback_mode = int(data["playbackOrder"])

        if isplaying or ispaused:
            current_song_id = data["playingItem"]
        else:
            #Currently stopped so try and use either the last playing song or the currently focused item
            if len(data["prevplayedItem"]) > 0:
                current_song_id = data["prevplayedItem"]
            else:
                current_song_id = data["focusedItem"]

        if current_song_id != "?":
            current_song_id = int(current_song_id)

        #Deriving the page ourselves because playlistPage is just whatever page is currently visible, not the page
        #that our song is actually on.
        if (data["playlistActive"] == data["playlistPlaying"]) or data["playingItem"] == "?" and current_song_id != "?":
            current_page = (current_song_id/int(data["playlistItemsPerPage"])) + 1
            cur_position_on_page = current_song_id - (current_page-1) * int(data["playlistItemsPerPage"])
            current_song_name = data["playlist"][cur_position_on_page]["t"]
            current_artist = data["playlist"][cur_position_on_page]["a"]
            try:
                next_song_in_playlist = data["playlist"][cur_position_on_page+1]["t"] + " - " + data["playlist"][cur_position_on_page+1]["a"]
            except:
                next_song_in_playlist = None
        else:
            if len(data["helper1"]) > 0:
                #Not on the correct playlist page, fall back to less reliable helperi fields
                current_song_name = re.match("^(.*) - $", data["helper1"]).group(1)
                current_artist = re.search("(.*) - %s" % re.escape(current_song_name), data["helper2"]).group(1)
                next_song_in_playlist = None
            else:
                return None

        return_data = {}
        return_data["isplaying"] = isplaying
        return_data["ispaused"] = ispaused
        return_data["playback_mode"] = playback_mode
        #Encountered a problem with the ajquery template returning HTML escape sequences in song/artist names
        #Hopefully this fixes it
        h = HTMLParser()
        return_data["song_name"] = unicode(h.unescape(current_song_name)).encode("utf8")
        return_data["artist_name"] = unicode(h.unescape(current_artist)).encode("utf8")
        return_data["next_song_in_playlist"] = next_song_in_playlist
        return return_data