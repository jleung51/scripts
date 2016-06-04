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

    # Prune this file
    f_temp = os.path.abspath(f)
    if f_temp == os.path.abspath(__file__):
        files.remove(f)
        continue

for f in files:
    print(f)
