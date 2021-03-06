
import eyed3
import logging
import requests
from pathlib import Path

from . import utils

log = logging.getLogger(__name__)

class Track:
	def __init__(self, session, data):
		self.session = session
		self.data = data

	@classmethod
	def from_id(cls, session, sid):
		"""
		Get a track from its ID

		:param session	: the session object to use
		:param sid		: the ID of the track
		"""
		resp = session.get(f"/tracks/{str(sid)}")
		resp.raise_for_status()

		data = resp.json()

		return cls(session, data)

	def raw_download(self, location):
		"""
		Download the MP3 of the track

		:param location	: the location to save the song to
		"""
		resp = self.session.get(self.data["media"]["transcodings"][1]["url"], raw=True)
		resp.raise_for_status()

		mp3_url = resp.json().get("url", None)

		file_size = 0

		with requests.get(mp3_url, stream=True) as resp:
			file_size = int(resp.headers.get("Content-Length", 0)) / 1024 / 1024
			with open(location, "wb") as file:
				for chunk in resp.iter_content(chunk_size=8192):
					file.write(chunk)

		log.debug("Finished downloading {:.2f}MB".format(file_size))

	def download(self, out_dir, raw_dir=False):
		"""
		Download and tag a track

		:param out_dir	: where to download the track to
		:param raw_dir	: whether or not to add the user's name to the location
		"""
		title = utils.format_song_name(self.data["title"])

		if raw_dir:
			location = out_dir
		else:
			location = f"{out_dir}/{self.data['user']['permalink']}"
			
		Path(location).mkdir(parents=True, exist_ok=True)

		target = f"{location}/{title}.mp3"

		self.raw_download(target)
		self.tag(target, album="Singles")

	def tag(self, location, track_num=None, track_total=None, album=None):
		"""
		Tag a given song using the track's data

		:param location		: location of the song to tag
		:param track_num  	: the track number of the song on a set
		:param track_total	: total amount of tracks on the set
		:param album		: the name of the set/album
		"""
		mp3 = eyed3.load(location)
		mp3.initTag()

		try:
			raw_artists = self.data["publisher_metadata"]["artist"]
		except (KeyError, TypeError):
			raw_artists = self.data["user"]["username"]

		artists = raw_artists.split(", ")

		mp3.tag.artist = "; ".join(artists)
		mp3.tag.artist_url = self.data["user"]["permalink"]
		mp3.tag.album = album
		mp3.tag.audio_source_url = self.data["permalink"]
		mp3.tag.audio_file_url = self.data["media"]["transcodings"][1]["url"]

		if self.data.get("created_at"):
			mp3.tag.release_date = self.data["created_at"][:4]
		else:
			mp3.tag.release_date = self.data["last_modified"][:4]

		mp3.tag.title = self.data["title"]
		mp3.tag.track_num = (track_num, track_total)

		if self.data.get("artwork_url"):
			resp = self.session.get(self.data["artwork_url"].replace("-large", "-t500x500"), raw=True)
		elif self.data["user"].get("avatar_url"):
			resp = self.session.get(self.data["user"]["avatar_url"].replace("-large", "-t500x500"), raw=True)
		else:
			resp = None

		if resp and resp.status_code == 200:
			mp3.tag.images.set(3, resp.content, "image/jpeg")

		mp3.tag.save()
