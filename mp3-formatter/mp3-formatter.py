#!/usr/bin/python3

import ID3
import os
import sys

mp3_extension = ".mp3"
names = ["final_name_1", "final_name_2", "final_name_3"]

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

if len(files) != len(names):
    raise RuntimeError(
        str(len(names)) +
        " file names were given but " +
        str(len(files)) +
        " files were found.")
    sys.exit()

files.sort()

print(files)
