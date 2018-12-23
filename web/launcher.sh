#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script

cd /
cd home/pi/bobweb/web
python3 manage.py runserver 0.0.0.0:8000 
