# encoding: utf-8
## fooBarLyrics.py - - Kyle Claisse - 2013
##
## This small program takes the currently playing song from foobar's COM interface and returns the lyrics for the song
#
# Revision 010 
# Last Modified: July 24, 2014
#

from time import time as tTime
from time import sleep 
import re, win32com.client
from lyricswiki import lyricswikiObj

#Age limit of the playlist cache before it grabs a new copy automatically. Default is 900 seconds (15 minutes)
#This will be overridden later when the settings are loaded or defauls are set. This is just a backup in case things go wrong.
_CACHE_AGE = 900

#Just a quick little function to straighten out some of the escaped parenthesis before displaying them.
#Works on strings and tuples
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


class lyricsClass:
	
	def __init__(self):
		self.songLyrics = None
		self.artist = None
		self.song = None
		self.last_song = None
		self.fbcom_handle = None
		self.fbcom_Playback = None
		self.manual_mode = {"manual": False, "song": "", "artist": "", "song_at_set": "", "search_mode": False, "search_url": ""} # [None,None] if not manual mode.[artist,song] when set manually
		self.playlist_database = {}
		self.lwobj = lyricswikiObj()
	
	def searchForLyrics(self, artist="", song=""):
		results = ""
		#Only search when we have something to match for the song. No artist-only searches.
		if len(song) > 1:
			results = self.lwobj.getLyrics(artist, song, search_mode=True)
		return results
	
	def resetManualEntry(self):
		print "Manual mode reset!"
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
		self.manual_mode["manual"] = True
		self.manual_mode["search_mode"] = True
		self.manual_mode["artist"] = url_split[2]
		self.manual_mode["song"] = url_split[1]
		self.manual_mode["search_url"] = url_split[0]
		self.update_current_track()
		self.manual_mode["song_at_set"] = self.song
	
	def manual_song_set(self, song_artist):
		if song_artist[0] and song_artist[1]:
			print "Querying artist and song manually..."
			self.manual_mode["manual"] = True
			self.manual_mode["artist"] = song_artist[0]
			self.manual_mode["song"] = song_artist[1]
			self.update_current_track()
			self.manual_mode["song_at_set"] = self.song
	
	def clear_playlist_cache(self):
		for x in self.playlist_database.keys():
			self.playlist_database[x][0] = 0
		print "Playlist cache cleared!"
	
	def setCacheAge(self, value):
		global _CACHE_AGE
		#Set the cache age
		_CACHE_AGE = value
	
	def setLWOps(self, opdict):
		self.lwobj.setInternalOptions(opdict)
	
	def get_statusbar_song(self, templates=None, selfie=False):
		#This function will either return the next song in the playlist (if playing in default order) or just returns the current song in nicely formatted order
		#Make sure we have a good com handle before we do anything, try to get it if its not active
		try:
			self.try_com()
			self.fbcom_handle
		except:
			return None

		#See if our playback method supports getting the next song in the list:
		if self.fbcom_Playback.Settings.ActivePlaybackOrder == u"Default" or "playlist" in self.fbcom_Playback.Settings.ActivePlaybackOrder:
			#Figure out the current playlist in use, see if we have that playlist cached or not
			current_playlist_index = self.fbcom_handle.Playlists.ActivePlaylist.Index
			try:
				self.playlist_database[current_playlist_index]
				if tTime() - self.playlist_database[current_playlist_index][0] > _CACHE_AGE:
					print "Playlist cache too old, updating..."
					raise Exception("Age limit exceeded")
				
			except:
				#We dont have that playlist in our cache so we should build it
				self.playlist_database[current_playlist_index] = [self.fbcom_handle.Playlists.ActivePlaylist.GetTracks("").Item(x).FormatTitle("%title%::%artist%") for x in range(int(self.fbcom_handle.Playlists.ActivePlaylist.GetSortedTracks("").Count))]
				self.playlist_database[current_playlist_index].insert(0, tTime()) #insert the current unix time in the first index position. This evens out the indexes (starting at 1 like in fbcom interface) and it helps keep track of the playlist cache age
			
			#Make a unicode string that contains our info like this song::artist
			unistring = unicode("%s::%s" % (_pUnescape(self.song), _pUnescape(self.artist)))
			next_song = ""
			#Now we check how many times unistring appears in the playlist_database at the current playlist's index. We only care if there is one match.
			if int(self.playlist_database[current_playlist_index].count(unistring)) == 1:
				current_song_index = self.playlist_database[current_playlist_index].index(unistring)
				#Figure out if we are at the end of the playlist
				if len(self.playlist_database[current_playlist_index]) == int(current_song_index+1):
					#Ok so we are at the end of our playlist, we don't have a next song to we're done.
					#Display the currently playing song and maybe add that its the end of the playlist
					next_song = "End of playlist:  %s - %s" % (self.song, self.artist)
					return _pUnescape(next_song)
					
				next_song_data = re.match("(?P<song>.*?)::(?P<artist>.*)", self.playlist_database[current_playlist_index][int(current_song_index+1)])
				next_song = "Next song:  %s - %s" % (next_song_data.group("song"), next_song_data.group("artist"))
			else:
				#There is more than one song in the playlist so we'll try and determine the song if we have any positional data to go on
				if self.last_song != None:
					#First we need to know how many instances there are and what their indices are
					new_indices = [i for i, x in enumerate(self.playlist_database[current_playlist_index]) if x == unistring]
					old_indices = [p for p, n in enumerate(self.playlist_database[current_playlist_index]) if n == self.last_song]
					#We're just going to compare the indices of the new song and the last song and see which of them are right next to each other.
					#If they are adjacent then the song after those two will be our next song. This is only accurate if playing continuously in
					#order and the user doesn't skip forward to a non-unique song in the playlist.
					for j in new_indices:
						for k in old_indices:
							if j-1 == k:
								nextsongdata = re.match("(?P<song>.*?)::(?P<artist>.*)", self.playlist_database[current_playlist_index][j+1])
								next_song = "Next song:  %s - %s" % (nextsongdata.group("song"), nextsongdata.group("artist"))
		if next_song == "":
			next_song = "Current song:  %s - %s" % (self.song, self.artist)
		return _pUnescape(next_song)
	
	def get_current_song_name(self):
		self.update_current_track()
		return _pUnescape(self.song)

	def get_songartist(self):
		self.update_current_track()
		if  self.song is not None: 
			song_info_tuple = (self.artist, self.song)
		elif self.fbcom_handle is None:
			song_info_tuple = ("Not connected to Fb2k COM server ", " Press refresh to reconnect")
		else:
			song_info_tuple = ("Undefined error", "please report")
			
		
		return _pUnescape(song_info_tuple)

	def try_com(self):
		try:			
			self.fbcom_handle = win32com.client.Dispatch("Foobar2000.Application.0.7") #Try to do this out of the main thread somehow, maybe using QThread or maybe with good ol' threading module
			self.fbcom_Playback = self.fbcom_handle.Playback
			return True
		except:
			self.fbcom_handle = None
			self.fbcom_Playback = None
			return False
	
	def end_com(self):
		self.fbcom_handle = None
		self.fbcom_Playback = None
	
	
	def update_current_track(self):
		#This will just update self.artist and self.song to the proper values if everything is working properly, it will
		#return None for both vars if the COM connection has failed and will return stop for both vars if no song is playing.
		
		#Start thinking about how we can override this function entirely and manually set the song manually.
		#We have to keep track of the current playing song still because when the song changes we still want to change the lyrics to the next song. 
		#In this instance we will assume the user has overridden our program because the lyrics are incorrect, incomplete, missing, or otherwise not what the user wants. 
		#
		try:
			self.fbcom_Playback.IsPlaying
		except:
			#COM connection has failed
			self.song = None
			self.artist = None
			return None
			
		if self.fbcom_handle is not None:
			if self.fbcom_Playback.IsPlaying:
				newsong = unicode(self.fbcom_Playback.FormatTitle("%title%")).encode("ascii", "ignore")
				newartist = unicode(self.fbcom_Playback.FormatTitle("%artist%")).encode("ascii", "ignore")
				newsong = newsong.replace("(", "\(")
				newsong = newsong.replace(")", "\)")
				#newsong = newsong.replace("\\", "\\\\")
				newartist = newartist.replace("(", "\(")
				newartist = newartist.replace(")", "\)")
				#we update the last song if the new one is different
				if newsong != self.song:
					#Ok the song has changed, we need to update the last song
					self.last_song = unicode("%s::%s" % (_pUnescape(self.song), _pUnescape(self.artist)))
				#A similar check for manual mode, has to be separate however for a single eventuality
				if self.manual_mode["manual"] == True and self.manual_mode["song_at_set"] not in newsong:
					self.manual_mode["manual"] = False
					self.manual_mode["search_mode"] = False
					self.manual_mode["song_at_set"] = ""
					self.manual_mode["song"] = ""
					self.manual_mode["url"] = ""
					self.manual_mode["artist"] = ""
				self.song = newsong #back to normal
				self.artist = newartist
				
			else: #Playback is stopped
				self.song = "stop"  #Setting these two vars to "stop" is what kicks the program into gear initially.
				self.artist = "stop" #At first, the check_song_loop does nothing until it sees "stop", then things start to happen
		else:
			self.song = None
			self.artist = None
			
		
		
	def getLyrics(self):
		if self.manual_mode["manual"] == True:
			artist = self.manual_mode["artist"]
			song = self.manual_mode["song"]
		else:
			artist = self.artist
			song = self.song
		
		try:
			if self.manual_mode["search_mode"] == True:
				self.songLyrics = self.lwobj.getLyrics(artist, song, manual_mode=self.manual_mode["manual"], search_url=self.manual_mode["search_url"])
			else:
				self.songLyrics = self.lwobj.getLyrics(artist, song, manual_mode=self.manual_mode["manual"])
		except Exception as error:
			print "DBG_B1"
			print error
			print "=======DBGB1======="
	
	def getLatestLyrics(self):
		self.update_current_track()
		if  self.song is not None and self.song != "stop":
			if  len(self.song) > 0:
				self.getLyrics()
			else:
				print "fb0dbg: song was an empty string"
				sleep(0.5)
				self.update_current_track()
				self.getLyrics()
		else:
			self.songLyrics = None
		return self.songLyrics
		
		
		