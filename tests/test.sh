#!/bin/sh

./cleanup.sh

FILES_PATH=../mp3-formatter
MP3_PATH=$FILES_PATH/mp3
URL=http://hikarinoakariost.info/koutetsujou-no-kabaneri-original-soundtrack/

i=1
until [ $i -ge 17 ]
do
    if [ $i -le 9 ];
    then
      touch $MP3_PATH/0$i.mp3
    else
      touch $MP3_PATH/$i.mp3
    fi

    i=`expr $i + 1`
done

cd $FILES_PATH
./mp3_formatter.sh $URL
