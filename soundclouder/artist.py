
import logging

from .set import Set
from .track import Track
from .constants import SC_API_URL_V2

log = logging.getLogger(__name__)

class Artist:
	def __init__(self, session, data):
		self.session = session
		self.data = data

	def raw_sets(self):
		sets = []
		offset = 0

		while 1:
			resp = self.session.get(f"/users/{str(self.data['id'])}/playlists", params={
				"offset": offset,
				"limit": 50
			})
			data = resp.json()

			for set in data["collection"]:
				sets.append(Set(self.session, set))

			if data.get("next_href"):
				offset += 50
			else:
				break

		log.debug(f"Got {str(len(sets))} sets")

		return sets

	def raw_tracks(self):
		tracks = []

		target_url = f"{SC_API_URL_V2}/users/{self.data['id']}/tracks"

		while 1:
			resp = self.session.get(target_url, raw=True)
			data = resp.json()

			for set in data["collection"]:
				tracks.append(Track(self.session, set))

			if data.get("next_href"):
				target_url = data["next_href"]
			else:
				break

		log.debug(f"Got {str(len(tracks))} tracks")

		return tracks

	def albums(self):
		sets = []

		for set in self.raw_sets():
			if set.data["is_album"] is True:
				sets.append(set)

		log.debug(f"Got {str(len(sets))} albums")

		return sets

	def playlists(self):
		sets = []

		for set in self.raw_sets():
			if set["is_album"] is False:
				sets.append(set)

		log.debug(f"Got {str(len(sets))} playlists")

		return sets

	def tracks(self):
		pass

	def favorites(self):
		return self.session.get(f"/users/{self.data['id']}/favorites").json()
