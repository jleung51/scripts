#!/bin/sh

# This sh script removes all files with the .mp3 extension from
# mp3-formatter/mp3, adds empty test mp3 files to that directory,
# then runs the mp3_formatter.sh script to rename and tag them with the
# artist and title.
#
# Run ./cleanup.sh afterwards to remove the leftover files.

./cleanup.sh

FILES_PATH=../mp3-formatter
MP3_PATH=$FILES_PATH/mp3
URL=http://hikarinoakariost.info/koutetsujou-no-kabaneri-original-soundtrack/
ARTIST="Hiroyuki Sawano"

i=1
until [ $i -ge 17 ]
do
    if [ $i -le 9 ];
    then
      cp file.mp3 $MP3_PATH/0$i.mp3
    else
      cp file.mp3 $MP3_PATH/$i.mp3
    fi

    i=`expr $i + 1`
done

cd $FILES_PATH
./mp3_formatter.sh "$URL" "$ARTIST"
