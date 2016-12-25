#!/usr/bin/python3

# This Python 3 file reads (from the command-line arguments) an artist name
# and (from stdin) a list of tracks, each separated by a newline, and
# renames the MP3 files in the mp3/ directory to "Artist - Title.mp3",
# in addition to ID3-tagging them with the artist and title.

import pytag
import os
import sys

def read_track_details():
    """Return the artist name and track names.

    Artist name must be the first line in the command-line argument.
    Track names must be inputted to stdin with newlines separating each
    name.
    """

    if len(sys.argv) < 2:  # sys.argv[0] is this script
        raise ValueError("No artist was given")
    sys.argv.pop(0)
    artist = ' '.join(sys.argv)

    tracklist = []
    for line in sys.stdin:
        tracklist.append(line.strip())  # Remove whitespace
    if not tracklist:
        raise ValueError("No track names were given")

    return artist, tracklist

def match_length(files, tracklist):
    """Raise error if the two lists have different lengths.
    """

    if len(files) != len(tracklist):
        raise RuntimeError(
            str(len(tracklist)) +
            " file names were given but " +
            str(len(files)) +
            " files were found.")

artist, tracklist = read_track_details()

mp3_extension = ".mp3"
mp3_location = "./mp3/"

files_all = os.listdir(mp3_location)
files = []

for f in files_all:

    # Prune directories
    if not os.path.isfile(mp3_location + f):
        continue

    # Prune non-MP3 files
    filename, extension = os.path.splitext(f)
    if extension != mp3_extension:
        continue

    # Prune this file
    f_temp = os.path.abspath(mp3_location + f)
    if f_temp == os.path.abspath(__file__):
        continue

    files.append(f)

match_length(files, tracklist)

files.sort()

i = 0
for f in files:

    file_id3 = pytag.Audio(os.path.abspath(mp3_location + f))
    file_id3.write_tags({ 'title' : tracklist[i], 'artist' : artist })
    # print(file_id3.get_tags())

    os.rename(
        mp3_location + f,
        mp3_location + artist + " - " + tracklist[i] + mp3_extension)

    i += 1
