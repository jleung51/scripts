#!/usr/bin/python3

import ID3
import os

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

files.sort()

print(files)
