#!/bin/sh
export FLASK_ENV=development
export FLASK_APP=wikichron_networks.py
export FLASK_RUN_PORT=5001
flask run
