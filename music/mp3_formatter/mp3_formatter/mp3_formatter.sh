#!/bin/sh

# This sh script scrapes a tracklist from www.hikarinoakariost.info
# (don't judge me) and renames all the MP3 files in the directory mp3/
# (assumed to be organized in correct track order) correspondingly,
# adding the name of the artist.

if [ "$1" = "--help" ] ; then
    echo "Usage: ./mp3_formatter.sh URL_TO_TRACKLIST ARTIST_NAME"
else
    ./url_scrape_div.py $1 | ./format_mp3.py $2
fi
