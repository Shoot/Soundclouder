
import os
import re
import logging

log = logging.getLogger(__name__)

def format_song_name(name):
	return re.sub(r'[\\/*?:"<>|]', "", name)

def load_client():
	appdata = os.getenv("LOCALAPPDATA")

	if appdata:
		local_file = appdata + "/soundclouder/client"
	else:
		local_file = "client"

	if os.path.isfile(local_file):
		with open(local_file, "r", encoding="utf-8") as file:
			data = file.read().strip()

		return data

def save_client(client_id):
	appdata = os.getenv("LOCALAPPDATA")
	
	if appdata:
		local_file = appdata + "/soundclouder/client"
	else:
		local_file = "client"
		
	with open(local_file, "w+", encoding="utf-8") as file:
		file.write(client_id)

def enumerate_download(artist, items, phrase, out_dir):
	log.info(f"Downloading all {phrase} from @{artist.data['permalink']}")

	for index, item in enumerate(items, start=1):
		log.info(f"[{str(index)}/{str(len(items))}] Downloading '{item.data['title']}'")
		item.download(out_dir)
