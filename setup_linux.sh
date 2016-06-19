#!/bin/sh

cd ~/Downloads/

sudo apt-get -y install curl git vim

./setup_guake.sh
./setup_ohmyzsh_agnoster.sh

./setup_wallpaper.sh
# ./setup_wallpaper_xubuntu.sh

./setup_manual_instructions.sh
