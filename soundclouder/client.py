
import json
from urllib.parse import urlparse

from .set import Set
from .track import Track
from .artist import Artist
from .session import Session
from .exceptions import InvalidURL

class Client:
	def __init__(self, client_id=None):
		self.session = Session(client_id)

	def resolve(self, url):
		"""
		Determine whether a given URL is for an artist, set, or track

		:param url 	: the URL to process
		"""
		url_info = urlparse(url)

		if not all([url_info.scheme, url_info.netloc]):
			raise InvalidURL("Invalid link was given")

		if url_info.netloc != "soundcloud.com":
			raise InvalidURL("URLs must come from Soundcloud")

		resp = self.session.get("/resolve", params={"url": url})
		data = resp.json()

		if not data:
			raise InvalidURL("Invalid Soundcloud URL")

		if data["kind"] == "playlist":
			return Set(self.session, data)
		elif data["kind"] == "user":
			return Artist(self.session, data)
		elif data["kind"] == "track":
			return Track(self.session, data)
		else:
			raise InvalidURL(f"Unknown kind: {data['kind']}")

	def me(self):
		"""
		Get the current user's data

		:no params:
		"""
		resp = self.session.get("/me")

		try:
			data = resp.json()
		except json.JSONDecodeError:
			data = {}

		return data
