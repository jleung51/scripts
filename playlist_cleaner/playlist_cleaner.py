#!/usr/bin/env python3
#
# This Python 3 script cleans up the song titles and artists from an M3U file.

import argparse
import os
import sys

if len(sys.argv) < 2:
    print("Error: Must input filename.")
    sys.exit(1)

current_dir = os.path.dirname(os.path.realpath(__file__))
with open(sys.argv[1], 'r') as fp:
    with open(current_dir + "/output.txt", 'w') as output_fp:
        line = fp.readline()
        while line:
            if line[0] == '#' and line.find(',') != -1:
                songstart = line.find(',') + 1
                output_fp.write(line[songstart:])
            line = fp.readline()
