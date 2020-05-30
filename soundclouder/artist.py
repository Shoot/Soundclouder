
import logging

from .set import Set
from .track import Track
from .constants import SC_API_URL_V2

log = logging.getLogger(__name__)

class Artist:
	def __init__(self, session, data):
		self.session = session
		self.data = data

	def fetch_collection(self, url):
		"""
		Fetch all items from a Soundcloud API collection

		:param url 	: the URL to get data from
		"""
		items = []

		target_url = SC_API_URL_V2 + url

		while 1:
			resp = self.session.get(target_url, raw=True)
			data = resp.json()

			for item in data["collection"]:
				item_type = item.get("type", "")
				item_kind = item.get("kind", "")

				if "track" in item_type or "comment" in item_kind:
					items.append(Track(self.session, item["track"]))
				elif "track" in item_kind:
					items.append(Track(self.session, item))
				elif "playlist" in item_type:
					items.append(Set(self.session, item["playlist"]))
				elif "playlist" in item_kind:
					items.append(Set(self.session, item))
				elif item_kind == "like":
					if item.get("track"):
						items.append(Track(self.session, item["track"]))
					elif item.get("playlist"):
						items.append(Set.from_id(self.session, item["playlist"]["id"]))
				else:
					log.debug(f"Unknown item type or kind: {item_type}:{item_kind}")

			if data.get("next_href"):
				target_url = data["next_href"]
			else:
				break

		log.debug(f"Got {str(len(items))} items for URL '{url}'")

		return items

	def raw_sets(self):
		"""
		Get all sets (incl. playlists and albums) from the artist

		:no params:
		"""
		return self.fetch_collection(f"/users/{str(self.data['id'])}/playlists")

	def raw_posts(self):
		"""
		Get all reposts and tracks from the user

		:no params:
		"""
		return self.fetch_collection(f"/profile/soundcloud:users:{self.data['id']}")

	def tracks(self):
		"""
		Get all of a user's own tracks

		:no params:
		"""
		return self.fetch_collection(f"/users/{self.data['id']}/tracks")

	def sets(self, album=True):
		"""
		Get all sets from an artist that are either an album/playlist

		:no params:
		"""
		sets = []

		for set in self.raw_sets():
			if set.data["is_album"] == album:
				sets.append(set)

		return sets

	def likes(self):
		"""
		All of a user's liked items, including sets and tracks

		:no params:
		"""
		return self.fetch_collection(f"/users/{self.data['id']}/likes")

	def comments(self):
		"""
		All tracks that a user has commented on

		:no params:
		"""
		return self.fetch_collection(f"/users/{self.data['id']}/comments")
