
import logging
from pathlib import Path

from . import utils
from .track import Track

log = logging.getLogger(__name__)

class Set:
	def __init__(self, session, data):
		self.session = session
		self.data = data

	@classmethod
	def from_id(cls, session, sid):
		"""
		Get a set from its ID

		:param session	: the session object to use
		:param sid		: the ID of the set
		"""
		resp = session.get(f"/playlists/{str(sid)}")
		resp.raise_for_status()

		data = resp.json()

		return cls(session, data)

	def tracks(self):
		"""
		Generate a list of tracks from the set

		:no params:
		"""
		tracks = []

		for item in self.data["tracks"]:
			if item.get("title"):
				tracks.append(Track(self.session, item))
			else:
				tracks.append(Track.from_id(self.session, item["id"]))

		log.debug(f"Got {str(len(tracks))} tracks")

		return tracks

	def download(self, location):
		"""
		Download all tracks from a set

		:param location: the location to save the tracks to
		"""
		location = f"{location}/{self.data['user']['permalink']}/sets/{self.data['permalink']}"
		Path(location).mkdir(parents=True, exist_ok=True)

		tracks = self.tracks()

		for index, track in enumerate(tracks, start=1):
			log.info(f"[{str(index)}/{str(len(tracks))}] Downloading '{track.data['title']}'")

			title = utils.format_song_name(track.data["title"])

			track.download(location, raw_dir=True)
			track.tag(
				f"{location}/{title}.mp3",
				track_num=index,
				track_total=len(tracks),
				album=self.data['title']
			)

		return tracks
