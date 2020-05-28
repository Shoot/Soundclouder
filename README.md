# Soundclouder
Download songs, sets, and all of an artist's releases from Soundcloud and tag them with ID3.

## Getting Started
### Prerequisites
* Python 3

### Installing
```
pip install git+git://github.com/Shoot/Soundclouder
```
Or clone this repository and type:
```
py setup.py install
```

## Usage
Type ``soundclouder -h`` for a full help list.
```
C:\>soundclouder -h
usage: __main__.py [-h] [-auth AUTH] [-file FILE] [-out OUT] [--debug]
                   [urls [urls ...]]

download soundcloud songs

positional arguments:
  urls        all of the songs you want to download

optional arguments:
  -h, --help  show this help message and exit
  -auth AUTH  your soundcloud client id, if none is given a new one will be
              generated
  -file FILE  load song url list from a file
  -out OUT    where to download files to
  --debug     display verbose debug information
```
An example of how you could use this is like the following:
```
soundclouder https://soundcloud.com/artist/song -out my_songs_folder
```
Running this would download the song "song" from user "artist" to the folder "my_songs_folder".

## Todo
- Improve README.md + docstrings
