#!/bin/sh

SCRIPTS="./sub-scripts"

cd ~/Downloads/

sudo apt-get -y install curl git vim

$SCRIPTS/setup_guake.sh
$SCRIPTS/setup_ohmyzsh_agnoster.sh

$SCRIPTS/setup_wallpaper.sh
# $SCRIPTS/setup_wallpaper_xubuntu.sh

$SCRIPTS/setup_manual_instructions.sh
