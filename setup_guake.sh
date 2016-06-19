#!/bin/sh

sudo apt-get -y install guake
gsettings set org.gnome.desktop.default-applications.terminal exec 'guake --new-tab'
gsettings set org.gnome.desktop.default-applications.terminal exec-arg '-e'
sudo cp /usr/share/applications/guake.desktop /etc/xdg/autostart/
cp files/guake.desktop ~/.config/autostart/
