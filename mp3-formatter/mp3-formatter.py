#!/usr/bin/python3

import ID3
import os

mp3_extension = ".mp3"

files = os.listdir('.')

for f in files:

    # Prune directories
    if not os.path.isfile(f):
        files.remove(f)
        continue

    # Prune non-MP3 files
    filename, extension = os.path.splitext(f)
    if extension != mp3_extension:
        files.remove(f)
        continue

    # Prune this file
    f_temp = os.path.abspath(f)
    if f_temp == os.path.abspath(__file__):
        files.remove(f)
        continue

print(files)
