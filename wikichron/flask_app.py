#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    flask_app.py

    Descp: Code for the Flask app

    Created on: 26-feb-2019

    Copyright 2019 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

from flask import Blueprint, render_template

server_bp = Blueprint('main', __name__)

@server_bp.route('/')
def index():
    return render_template("index.html", title='Home Page')




