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
import flask
import flask
from flask import Blueprint, current_app

# Imports from dash apps
# classic
import wikichron.dash.apps.classic.metrics.interface as classic_interface
import wikichron.dash.apps.classic.data_controller as classic_data_controller
# networks
import wikichron.dash.apps.networks.networks.interface as networks_interface
import wikichron.dash.apps.networks.data_controller as networks_data_controller


server_bp = Blueprint('main', __name__)


@server_bp.route('/')
@server_bp.route('/welcome.html')
def index():
    config = current_app.config;

    return flask.render_template("welcome.html",
                                development = config["DEBUG"],
                                title = 'WikiChron - Welcome')


@server_bp.route('/classic/') #TOMOVE to BP
@server_bp.route('/classic/selection') #TOMOVE to BP
def classic_app():

    def transform_metric_obj_in_metric_frontend(metric):
        return {'name': metric.text,
                'code': metric.code,
                'descp': metric.descp,
                'category': metric.category}

    config = current_app.config;

    wikis = classic_data_controller.get_available_wikis()

    metrics_by_category_backend = classic_interface.get_available_metrics_by_category()
    # transform metric objects to a dict with the info we need for metrics:
    categories_frontend = {}
    for (cat_obj, cat_metrics) in metrics_by_category_backend.items():
        cat_name = cat_obj.value
        categories_frontend[cat_name] = [transform_metric_obj_in_metric_frontend(metric) for metric in cat_metrics]

    return flask.render_template("classic/selection/selection.html",
                                title = 'WikiChron Classic - selection',
                                development = config["DEBUG"],
                                wikis = wikis,
                                categories = categories_frontend)


@server_bp.route('/networks/') #TOMOVE to BP
@server_bp.route('/networks/selection') #TOMOVE to BP
def networks_app():

    config = current_app.config;

    wikis = networks_data_controller.get_available_wikis()

    network_backend_objects = networks_interface.get_available_networks()
    networks_frontend = []
    for nw in network_backend_objects:
        networks_frontend.append({ 'name': nw.NAME, 'code': nw.CODE})

    return flask.render_template("networks/selection/selection.html",
                                title = 'WikiChron Networks - selection',
                                development = config["DEBUG"],
                                wikis = wikis,
                                networks = networks_frontend)


#--------- BEGIN AUX SERVERS (non pure flask / jinja / html / http servers) ---#

#--- JS server ----#

# Serve js/ folder
local_js_directory = 'js/'

@server_bp.route('/js/<js_file>', defaults={'path': ''})
@server_bp.route('/js/<path:path>/<js_file>')
def serve_local_js(path, js_file):
    js_directory = os.path.join(local_js_directory, path)
    print ('Returning javascript file: {}'.format(js_file))
    return flask.send_from_directory(js_directory, js_file)


# Serve lib/ folder only in development mode
@server_bp.route('/lib/<dep>', defaults={'path': ''})
@server_bp.route('/lib/<path:path>/<dep>')
def serve_lib_in_dev(path, dep):
    path = os.path.join('lib/', path)
    dev = current_app.config["DEBUG"]
    if dev:
        return flask.send_from_directory(path, dep)
    else:
        print('Trying to retrieve a dependency from a local folder in production. Skipping.')


