import os
import logging
import argparse
from pathlib import Path

from . import utils
from .set import Set
from .track import Track
from .artist import Artist
from .client import Client

log = logging.getLogger(__name__)

def main():
	parser = argparse.ArgumentParser(description="download soundcloud songs")

	parser.add_argument("-auth", help="your soundcloud client id, if none is given a new one will be generated", default=None)
	parser.add_argument("-file", help="load song url list from a file")
	parser.add_argument("-out", help="where to download files to", default="./songs")
	parser.add_argument("--debug", help="display verbose debug information", action="store_true", default=False)
	parser.add_argument("urls", nargs="*", help="all of the songs you want to download", default=None)

	args = parser.parse_args()

	logging_config = {
		"format": "[%(asctime)s] %(levelname)s: %(message)s",
		"datefmt": "%H:%M:%S"
	}

	logging.getLogger("chardet").setLevel(logging.WARNING)
	logging.getLogger("urllib3").setLevel(logging.WARNING)
	logging.getLogger("eyed3").setLevel(logging.WARNING)

	if args.debug:
		logging_config["level"] = logging.DEBUG
	else:
		logging_config["level"] = logging.INFO

	logging.basicConfig(**logging_config)

	urls = []

	if args.urls:
		urls += args.urls

	if args.file:
		if os.path.isfile(args.file):
			with open(args.file, "r", encoding="utf-8") as file:
				urls += file.read().split("\n")
		else:
			log.critical("Invalid song list file")

	if len(urls) == 0:
		log.critical("No songs were given")
		quit()

	client = Client(args.auth)

	out_dir = args.out.rstrip("/")

	for url in args.urls:
		item = client.resolve(url.rstrip("/"))
		log.debug(f"Processed '{url}' with type '{type(item)}'")

		if isinstance(item, Artist):
			log.info(f"Downloading all items from @{item.data['permalink']}")

			albums = item.albums()
			dl_history = []

			for album in albums:
				log.info(f"Downloading all tracks from @{item.data['permalink']} - {album.data['title']}")

				location = f"{out_dir}/{item.data['permalink']}/sets/{album.data['permalink']}"
				Path(location).mkdir(parents=True, exist_ok=True)

				album.download(location)

			tracks = item.raw_tracks()

			for index, track in enumerate(tracks, start=1):
				if track.data['permalink'] in dl_history:
					log.debug(f"Removed '{track.data['title']}' as it has already been downloaded")
					continue

				log.info(f"[{str(index)}/{str(len(tracks))}] Downloading '{track.data['title']}'")

				title = utils.format_song_name(track.data["title"])

				location = f"{out_dir}/{track.data['user']['permalink']}"
				Path(location).mkdir(parents=True, exist_ok=True)

				target = f"{location}/{title}.mp3"

				track.download(target)
				track.tag(target, album="Singles")

			log.info(f"Downloaded everything from @{item.data['permalink']}")
		elif isinstance(item, Track):
			title = utils.format_song_name(item.data["title"])

			location = f"{out_dir}/{item.data['user']['permalink']}"
			Path(location).mkdir(parents=True, exist_ok=True)

			target = f"{location}/{title}.mp3"

			log.info(f"Downloading '{item.data['title']}'")

			item.download(target)
			item.tag(target, album="Singles")
		elif isinstance(item, Set):
			location = f"{out_dir}/{item.data['user']['permalink']}/sets/{item.data['permalink']}"
			Path(location).mkdir(parents=True, exist_ok=True)

			item.download(location)
		else:
			log.error("Invalid URL was given")

	log.info("Finished downloading all items")

if __name__ == "__main__":
	main()