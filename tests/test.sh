#!/bin/sh

./cleanup.sh

FILES_PATH=../mp3-formatter
URL=http://hikarinoakariost.info/koutetsujou-no-kabaneri-original-soundtrack/

i=1
until [ $i -ge 17 ]
do
    if [ $i -le 9 ];
    then
      touch $FILES_PATH/0$i.mp3
    else
      touch $FILES_PATH/$i.mp3
    fi

    i=`expr $i + 1`
done

cd $FILES_PATH
./url_scrape_div.py $URL | ./rename_mp3.py
