#!/bin/sh

# This sh script removes all files in the mp3-formatter/mp3/ directory.
#
# Usage: ./cleanup.sh

FILES_PATH=../mp3-formatter/mp3
rm -f $FILES_PATH/*.mp3
