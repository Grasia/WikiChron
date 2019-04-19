#!/bin/bash
git pull origin master &&
if [ -e venv.old/ ]; then
  rm -r venv.old/
fi  
mv venv/ venv.old/ &&
virtualenv -p python3 venv/ &&
source venv/bin/activate &&
bash install.sh &&
gunicorn wikichron_launcher:server -c gunicorn_config.py
