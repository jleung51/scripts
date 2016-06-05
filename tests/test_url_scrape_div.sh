#!/bin/sh

# This sh script scrapes a tracklist from a specific URL, removes excess
# content and numbering/whitespace, and prints out the results.

FILES_PATH=../mp3-formatter
URL=http://hikarinoakariost.info/koutetsujou-no-kabaneri-original-soundtrack/

cd $FILES_PATH
./url_scrape_div.py "$URL"
