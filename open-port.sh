#!/bin/sh
#
# This shell script opens a local port by adding an exception to the
# firewall rules.
#
# For more information, see:
#   https://www.digitalocean.com/community/tutorials/how-to-list-and-delete-iptables-firewall-rules
#

if [ $# -ge 1 ] ; then
  sudo iptables -I INPUT -p tcp --dport $1 --syn -j ACCEPT
  sudo service iptables save
  echo "Please reboot to allow the firewall changes to take effect."
else
  echo "Usage: ./open-port.sh port"
fi
