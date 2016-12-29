#!/bin/sh

if [ $# -ge 1 ] ; then
  sudo chkconfig $1 off
else
  echo "Usage: ./stop_autostart_service.sh service_name"
fi
