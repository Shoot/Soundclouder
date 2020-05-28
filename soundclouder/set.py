
import logging

from . import utils
from .track import Track

log = logging.getLogger(__name__)

class Set:
	def __init__(self, session, data):
		self.session = session
		self.data = data

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
		tracks = self.tracks()

		for index, track in enumerate(tracks, start=1):
			log.info(f"[{str(index)}/{str(len(tracks))}] Downloading '{track.data['title']}'")

			title = utils.format_song_name(track.data["title"])
			target = f"{location}/{title}.mp3"

			track.download(target)
			track.tag(
				target,
				track_num=index,
				track_total=len(tracks),
				album=self.data['title']
			)

		return tracks