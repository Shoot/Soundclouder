class NoClientID(Exception):
	""" No valid client ID was given """
	pass

class InvalidURL(Exception):
	""" Given URL was invalid and/or not from Soundcloud """
	pass

class InvalidID(Exception):
	""" Given song/set/artist ID does not exist or is invalid """
	pass
