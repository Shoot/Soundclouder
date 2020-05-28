
import os
import re

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