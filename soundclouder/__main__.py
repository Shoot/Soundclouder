import os
import logging
import argparse

from . import utils
from .set import Set
from .track import Track
from .artist import Artist
from .client import Client

log = logging.getLogger(__name__)

def main():
	parser = argparse.ArgumentParser(description="download soundcloud songs")

	parser.add_argument("-a", "--auth", help="your soundcloud client id, if none is given a new one will be generated", default=None)
	parser.add_argument("-f", "--file", help="load song url list from a file", default=None)
	parser.add_argument("-o", "--out", help="where to download files to", default="./songs")
	parser.add_argument("--albums", help="download all of a user's albums", action="store_true", default=False)
	parser.add_argument("--all-posts", help="download all tracks (incl. reposted) from a user", action="store_true", default=False)
	parser.add_argument("--comments", help="download songs that the user commented on", action="store_true", default=False)
	parser.add_argument("--debug", help="display verbose debug information", action="store_true", default=False)
	parser.add_argument("--likes", help="download songs from a user's likes", action="store_true", default=False)
	parser.add_argument("--no-reposts", help="only download a user's songs, no reposts", action="store_true", default=False)
	parser.add_argument("--playlists", help="download all of a user's playlists", action="store_true", default=False)
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
			if args.albums and args.playlists:
				utils.enumerate_download(item, item.raw_sets(), "sets", out_dir)
			elif args.albums:
				utils.enumerate_download(item, item.sets(album=True), "albums", out_dir)
			elif args.playlists:
				utils.enumerate_download(item, item.sets(album=False), "playlists", out_dir)

			if args.no_reposts:
				utils.enumerate_download(item, item.tracks(), "posts (no reposts)", out_dir)
			elif args.all_posts:
				utils.enumerate_download(item, item.raw_posts(), "posts", out_dir)

			if args.comments:
				utils.enumerate_download(item, item.comments(), "commented posts", out_dir)

			if args.likes:
				utils.enumerate_download(item, item.likes(), "liked posts", out_dir)
		elif isinstance(item, Track):
			log.info(f"Downloading '{item.data['title']}'")
			item.download(out_dir)
		elif isinstance(item, Set):
			log.info(f"Downloading all tracks from @{item.data['user']['permalink']} - '{item.data['title']}'")
			item.download(out_dir)
		else:
			log.error("Invalid URL was given")

	log.info("Finished downloading all items")

if __name__ == "__main__":
	main()
