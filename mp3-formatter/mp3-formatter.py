#!/usr/bin/python3

import ID3
import os

mp3_extension = ".mp3"

files = os.listdir('.')

for f in files:
    if not os.path.isfile(f):
        files.remove(f)
    else:
        f = os.path.abspath(f)

for f in files:
    print(f)
