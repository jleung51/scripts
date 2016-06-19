#!/bin/sh

cd ~/Downloads/

sudo apt-get -y install curl git vim

./setup_guake.sh
./setup_ohmyzsh_agnoster.sh

./setup_wallpaper.sh
# ./setup_wallpaper_xubuntu.sh

# Manual
#guake --preferences
#	General:
#		Disable popup notifications on startup
#	Shell:
#		Set default interpreter to /bin/zsh
#	Appearance:
#		Disable "Use the system fixed width font"
#		Select Font: "Meslo LG M DZ for Powerline RegularForPowerline"
#		Select Palette - Built-in scheme: "Tomorrow Night Blue"
#		Set Transparency: 25%
#
#http://askubuntu.com/questions/412982/where-can-i-download-xubuntu-released-wallpapers
