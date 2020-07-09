#!/usr/bin/env python3
# This Python 3 script replaces text in a file, in-place.

# For Windows, use:
#!python

import fileinput
import os
import sys

def isValidFile(filename):
    return (filename.lower().endswith('.m3u') or
            filename.lower().endswith('.m3u8'))

def processFile(filename):
    '''Makes custom text modifications to a single file.

    Returns true if modified, false if not modified.
    '''

    modified = False

    with fileinput.input(filename, inplace=True) as f:
        for line in f:

            # Check any condition
            if '\\' in line:
                modified = True

            # Make the modifications
            newline = line.replace('\\', '/')
            sys.stdout.write(newline)

    return modified


if __name__ == '__main__':
    for filename in os.listdir(os.getcwd()):
        if not isValidFile(filename):
            continue

        modified = processFile(filename)
        if modified:
            print(filename)

    # Wait for user input to finish
    input()