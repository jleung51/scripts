#!/bin/sh

if [ $# -ge 1 ] ; then
  sudo chkconfig --add $1
  sudo chkconfig $1 on
else
  echo "Usage: ./autostart_service.sh service_name"
fi
