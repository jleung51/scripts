#!/bin/sh

xfconf-query --channel xfce4-desktop --property /backdrop/screen0/monitor0/image-path --set ~/Pictures/Wallpapers/Mountainous_View_by_Sven_Scheuermier.jpg
xfdesktop --reload
