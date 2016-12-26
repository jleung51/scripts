#!/bin/sh

sudo apt-get -y install zsh

# oh-my-zsh
sudo apt-get -y install curl
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
sed -i 's/ZSH_THEME.*/ZSH_THEME="agnoster"/g' ~/.zshrc

# agnoster font
sudo wget -P /usr/share/fonts/opentype https://github.com/powerline/fonts/raw/master/Meslo/Meslo%20LG%20M%20DZ%20Regular%20for%20Powerline.otf
fc-cache -fv
