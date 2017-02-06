#!/bin/sh

cd $(dirname $0)/src

./dropbox_download.py
./pcloud_upload.py
./gdrive_upload.py
