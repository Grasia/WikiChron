#!/bin/sh
export FLASK_ENV=development
export FLASK_APP=wikichron.py
export FLASK_RUN_PORT=5002
flask run
