#!/bin/sh

sudo apt-get -y install xubuntu-community-wallpapers

mkdir -p ~/Pictures/Wallpapers/
cp /usr/share/xfce4/backdrops/Mountainous_View_by_Sven_Scheuermeier.jpg ~/Pictures/Wallpapers/

gsettings set org.gnome.desktop.background picture-uri file://~/Pictures/Wallpapers/Mountainous_View_by_Sven_Scheuermeier.jpg
