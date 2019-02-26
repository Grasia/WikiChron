#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    flask_app.py

    Descp: Code for the Flask app

    Created on: 26-feb-2019

    Copyright 2019 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

import os
from urllib.parse import urljoin
from flask import Blueprint, render_template, redirect, send_from_directory

server_bp = Blueprint('main', __name__)

wikichron_base_pathname = '/app/'; #TOCHANGE use config var


# Redirects / to /app
@server_bp.route('/')
@server_bp.route('/index.html')
def redirect_index_to_app():
    print('Redirecting user to {}...'.format(wikichron_base_pathname))
    return redirect(wikichron_base_pathname, code=302)


@server_bp.route('/welcome.html')
def index():
    return render_template("index.html", title='Home Page')


#--------- BEGIN AUX SERVERS (non pure flask / jinja / html / http servers) ---#

#--- JS server ----#

# js files being serve by this server:
local_available_js = [
    'side_bar.js',
    'controls_side_bar.js',
    'main.share_modal.js',
    'piwik.js'
]

# Serve js/ folder
local_js_directory = 'js/'
js_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            local_js_directory)

@server_bp.route('/js/<js_path>.js')
def serve_local_js(js_path):
    js_name = f'{js_path}.js'
    if js_name not in local_available_js:
        raise Exception(
            '"{}" is excluded from the allowed static files'.format(
                js_path
            )
        )
    print ('Returning: {}'.format(js_name))
    return send_from_directory(js_directory, js_name)

