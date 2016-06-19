#!/bin/sh

cd ~/Downloads/

sudo apt-get -y install curl git vim

sudo apt-get -y install guake
gsettings set org.gnome.desktop.default-applications.terminal exec 'guake --new-tab'
gsettings set org.gnome.desktop.default-applications.terminal exec-arg '-e'
sudo cp /usr/share/applications/guake.desktop /etc/xdg/autostart/
cp guake.desktop ~/.config/autostart/guake.desktop

sudo apt-get -y install xubuntu-community-wallpapers
mkdir ~/Pictures/Wallpapers
cp /usr/share/xfce4/backdrops/Mountainous_View_by_Sven_Scheuermier.jpg ~/Pictures/Wallpapers/
gsettings set org.gnome.desktop.background picture-uri file://~/Pictures/Wallpapers/Mountainous_View_by_Sven_Scheuermier.jpg

sudo apt-get -y install zsh
# oh-my-zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
sed -i 's/ZSH_THEME.*/ZSH_THEME="agnoster"/g' ~/.zshrc
# agnoster font
sudo wget -P /usr/share/fonts/opentype https://github.com/powerline/fonts/raw/master/Meslo/Meslo%20LG%20M%20DZ%20Regular%20for%20Powerline.otf
fc-cache -fv

# Xubuntu

#xfconf-query --channel xfce4-desktop --property /backdrop/screen0/monitor0/image-path --set ~/Pictures/Wallpapers/Mountainous_View_by_Sven_Scheuermier.jpg
#xfdesktop --reload


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
