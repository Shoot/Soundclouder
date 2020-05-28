
import re
import logging
import requests
from bs4 import BeautifulSoup

from . import utils
from .constants import SC_BASE_URL, SC_API_URL_V2
from .exceptions import NoClientID

log = logging.getLogger(__name__)

class Session:
	def __init__(self, client_id=None):
		self.session = requests.Session()

		self.client_id = None

		if client_id in {'', None}:
			self.client_id = self.new_client_id()
		else:
			self.client_id = client_id

	def new_client_id(self):
		"""
		Generate a fresh client ID for a guest user

		:no params:
		"""
		client_id = utils.load_client()

		if client_id != None:
			log.debug(f"Loaded a local client ID: {client_id}")
			resp = self.get("/me", params={"client_id": client_id})

			if resp.status_code == 200:
				log.debug("Local client ID is working")
				return client_id

			log.debug("Local client ID is unauthenticated or does not work")

		log.debug("Generating a new client ID...")

		resp = self.session.get(SC_BASE_URL)
		soup = BeautifulSoup(resp.text, "html.parser")

		scripts = soup.find_all("script", crossorigin=True)
		for script in scripts:
			resp = self.session.get(script.get("src"))
			search = re.search("\?client_id=(\\b\w{32}\\b)&", resp.text)

			if search:
				client_id = search.group(1)
				break

		if client_id is None:
			raise NoClientID()

		log.debug(f"Generated a new client ID: '{client_id}'")

		utils.save_client(client_id)

		return client_id

	def get(self, url, raw=False, **kwargs):
		"""
		Perform a GET request on a url

		:param url 		: the URL to get from
		:param raw		: whether or not to add the base API url to the front of the
					  	  URL. Raw URLs will not be added to.
		:param kwargs	: any more arguments to give to the request
		"""
		if raw:
			target_url = url
		else:
			target_url = SC_API_URL_V2 + url

		if kwargs.get("params"):
			if not kwargs["params"].get("client_id"):
				kwargs["params"]["client_id"] = self.client_id
		else:
			kwargs["params"] = {"client_id": self.client_id}

		return self.session.get(target_url, params=kwargs["params"])
