#!/bin/sh

# This sh script removes all files with the .mp3 extension from
# mp3-formatter/mp3, adds empty test mp3 files to that directory,
# then runs the mp3_formatter.sh script to rename and tag them with the
# artist and title.

FILES_PATH=../mp3-formatter
URL=http://hikarinoakariost.info/koutetsujou-no-kabaneri-original-soundtrack/

cd $FILES_PATH
./url_scrape_div.py "$URL"
