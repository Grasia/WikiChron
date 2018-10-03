#!/bin/sh
(git pull origin master && pkill -HUP gunicorn) || (gunicorn wikichron:server -c gunicorn_config.py)
