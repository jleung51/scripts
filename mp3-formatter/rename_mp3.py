#!/usr/bin/python3

# This Python 3 file reads (from stdin) a list of tracks, each separated by
# a newline, and renames the MP3 files in the current folder to the tracklist.

import ID3
import os
import sys

def read_tracklist():
    """Return list of tracks from stdin.
    """

    tracklist = []
    for line in sys.stdin:
        tracklist.append(line)
    return tracklist

def match_length(files, tracklist):
    """Raise error if the two lists have different lengths.
    """

    if len(files) != len(tracklist):
        raise RuntimeError(
            str(len(tracklist)) +
            " file names were given but " +
            str(len(files)) +
            " files were found.")

tracklist = read_tracklist()
mp3_extension = ".mp3"

files_all = os.listdir('.')
files = []

for f in files_all:

    # Prune directories
    if not os.path.isfile(f):
        continue

    # Prune non-MP3 files
    filename, extension = os.path.splitext(f)
    if extension != mp3_extension:
        continue

    # Prune this file
    f_temp = os.path.abspath(f)
    if f_temp == os.path.abspath(__file__):
        continue

    files.append(f)

match_length(files, tracklist)

files.sort()

i = 0
for f in files:
    os.rename(f, tracklist[i] + mp3_extension)
    i += 1
