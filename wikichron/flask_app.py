#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    flask_app.py

    Descp: Code for the Flask app

    Created on: 26-feb-2019

    Copyright 2019 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

from flask import Blueprint, render_template, redirect

server_bp = Blueprint('main', __name__)

wikichron_base_pathname = '/app/';

# Redirects / to /app
@server_bp.route('/')
@server_bp.route('/index.html')
def redirect_index_to_app():
    print('Redirecting user to {}...'.format(wikichron_base_pathname))
    return redirect(wikichron_base_pathname, code=302)


@server_bp.route('/welcome.html')
def index():
    return render_template("index.html", title='Home Page')




