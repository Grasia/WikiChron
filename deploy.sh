#!/bin/sh
gunicorn wikichron:server -c gunicorn_config.py
