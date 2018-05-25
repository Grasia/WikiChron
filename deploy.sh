#!/bin/sh
(git pull origin master && pkill -HUP gunicorn) || (gunicorn app:server -c gunicorn_config.py)
