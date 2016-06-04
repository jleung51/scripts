#!/bin/sh

# This sh script scrapes a tracklist from www.hikarinoakariost.info
# (don't judge me) and renames all the MP3 files in the current directory
# (assumed to be organized in correct track order) correspondingly.

if [ "$1" = "--help" ] ; then
    echo "Usage: ./mp3_formatter.sh URL_TO_TRACKLIST"
else
    ./url_scrape_div.py $1 | ./rename_mp3.py
fi
