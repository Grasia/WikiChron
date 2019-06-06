#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    flask_app.py

    Descp: Code for the Flask app

    Created on: 26-feb-2019

    Copyright 2019 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

# built-in imports
import os
import datetime
from urllib.parse import urljoin
import flask
from flask import Blueprint, current_app, request, jsonify, url_for, redirect
from werkzeug.utils import secure_filename
import shutil

# local imports
import wikichron.utils.data_manager as data_manager
import wikichron.utils.utils as utils

# Imports from dash apps
# classic
import wikichron.dash.apps.classic.metrics.interface as classic_interface
# networks
import wikichron.dash.apps.networks.networks.interface as networks_interface

# upload config variables
ALLOWED_EXTENSIONS = set(['csv'])

server_bp = Blueprint('main', __name__)


@server_bp.route('/')
@server_bp.route('/welcome.html')
def index():
    config = current_app.config;

    return flask.render_template("welcome.html",
                                development = config["DEBUG"],
                                title = 'WikiChron - Welcome')


@server_bp.route('/classic/') #TOMOVE to BP # will be wizard screen
@server_bp.route('/classic/selection') #TOMOVE to BP
def classic_app():

    def transform_metric_obj_in_metric_frontend(metric):
        return {'name': metric.text,
                'code': metric.code,
                'descp': metric.descp,
                'category': metric.category}

    config = current_app.config;

    wikis = data_manager.get_available_wikis()

    metrics_by_category_backend = classic_interface.get_available_metrics_by_category()
    # transform metric objects to a dict with the info we need for metrics:
    categories_frontend = {}
    for (cat_obj, cat_metrics) in metrics_by_category_backend.items():
        cat_name = cat_obj.value
        categories_frontend[cat_name] = [transform_metric_obj_in_metric_frontend(metric) for metric in cat_metrics]

    # take all wikis and metrics in query string
    selected_wikis   = set(request.args.getlist('wikis'))
    selected_metrics = set(request.args.getlist('metrics'))

    return flask.render_template("classic/selection/selection.html",
                                title = 'WikiChron Classic - selection',
                                mode = 'classic',
                                development = config["DEBUG"],
                                wikis = wikis,
                                categories = categories_frontend,
                                pre_selected_wikis = selected_wikis,
                                pre_selected_metrics = selected_metrics,
                                )


@server_bp.route('/networks/') #TOMOVE to BP # will be wizard screen
@server_bp.route('/networks/selection') #TOMOVE to BP
def networks_app():

    config = current_app.config;

    wikis = data_manager.get_available_wikis()

    network_backend_objects = networks_interface.get_available_networks()
    networks_frontend = []
    for nw in network_backend_objects:
        networks_frontend.append({ 'name': nw.NAME, 'code': nw.CODE})

    # take only the first one in case more than one
    selected_wikis    = request.args.get('wikis', default=set(), type=str)
    selected_networks = request.args.get('network', default=set(), type=str)

    return flask.render_template("networks/selection/selection.html",
                                title = 'WikiChron Networks - selection',
                                mode = 'networks',
                                development = config["DEBUG"],
                                wikis = wikis,
                                networks = networks_frontend,
                                pre_selected_wikis = selected_wikis,
                                pre_selected_networks = selected_networks
                                )


@server_bp.route('/upload')
@server_bp.route('/upload.html')
def upload():
    config = current_app.config;

    return flask.render_template("upload.html",
                                development = config["DEBUG"],
                                title = 'WikiChron - Upload a wiki')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@server_bp.route('/csv-upload', methods = ['POST'])
def upload_post():

    def upload_error(msg):
        print(msg)
        html = msg + '<p><a href="/upload.html">Go back</a></p>'
        return html, 400

    config = current_app.config

    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            #~ flash('Missing file part')
            msg = 'Missing file part'
            #~ return redirect(url_for('.upload'))
            return upload_error(msg)

        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            #~ flash('No selected file')
            #~ return redirect(url_for('.upload'))
            msg = 'No selected file'
            return upload_error(msg)

        if not allowed_file(file.filename):
            msg = 'File extension not supported.'
            #~ flash('File extension not supported.')
            #~ return redirect(url_for('.upload'))
            return upload_error(msg)

        wikis = data_manager.get_available_wikis()

        # check wiki url if wiki is already there. if what's there is "verified" then cancel.
        wiki_url = request.form['url']
        try:
            wiki_domain = utils.get_domain_from_url(wiki_url)
        except:
            return upload_error('Unrecognized format for url. Please, prepend the url with http:// or https://')

        domains = [wiki['domain'] for wiki in wikis]

        overwriting_existing = False

        if wiki_domain in domains:

            existing_wiki = wikis[domains.index(wiki_domain)]

            if 'verified' in existing_wiki and existing_wiki['verified']:
                return upload_error(f'Wiki {wiki_domain} is verified. Verified data cannot be overwritten by guest users.')

            else:
                overwriting_existing = True
                return upload_error('Caution! overwriting existing wiki!') # confirm overwriting

        # Set filename
        filename = wiki_domain + '.csv'
        filename = secure_filename(filename)

        # If overwriting existing wiki, move old data to old/date/filename.
        if overwriting_existing:
            backup_dir = os.path.join('old', existing_wiki['lastUpdated'])
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            shutil.move(existing_wiki['data'], backup_dir)


        # store file in FS
        file.save(os.path.join(config['UPLOAD_FOLDER'], filename))

        # process csv, check for errors generate wikis.json metadata
        try:
            wiki_df = data_manager.load_dataframe_from_csv(filename)
            wiki_stats = data_manager.get_stats(wiki_df)
        except:
            os.remove(os.path.join(config['UPLOAD_FOLDER'], filename))
            return upload_error('The provided csv file has an invalid format. Please, use our parser to parse the xml dump file.')

        # Set lastUpdated value
        if 'date' in request.form and request.form['date'] <= str(datetime.date.today()):
            date = request.form['date']
        else: # If invalid or not provided, just set it to 'NA'
            date = 'NA'

        # show previous stats and ask confirmation to the user. Wait for user confirmation
        wiki_name = request.form['name']
        new_wiki = {
            "url": wiki_url,
            "domain": wiki_domain,
            "data": filename,
            "name": wiki_name,
            "lastUpdated": date,
            "uploadedBy": request.remote_addr,
            "verified": False
        }
        new_wiki.update(wiki_stats)

        print(new_wiki)

        # update wikis.json
        wikis.append(new_wiki)

        if not data_manager.update_wikis_metadata(wikis):
            return upload_error('Error updating wiki metadata. Please, try again.')




        # Redirect to upload-success
        return redirect(url_for('.list_data'))



    else:
        msg = 'HTTP method not expected'
        #~ flash('HTTP method not expected')
        #~ return redirect(url_for('.upload'))
        return upload_error(msg)


    return flask.render_template("upload-success.html",
                                development = config["DEBUG"],
                                title = 'WikiChron - Successful upload!')

    return flask.render_template("upload-error.html",
                                development = config["DEBUG"],
                                title = 'WikiChron - Upload error!')


@server_bp.route('/data')
@server_bp.route('/list_data')
def list_data():
    wikis = data_manager.get_available_wikis()

    config = current_app.config

    return flask.render_template("data.html",
                            title = 'WikiChron - available wikis',
                            development = config["DEBUG"],
                            wikis = wikis
                            )


@server_bp.route('/wikisTimelifes.json')
def serve_wikis_time_lifes():

    wikis = data_manager.get_available_wikis()

    time_spans = { wiki['domain']: {'first_date': wiki['first_edit']['date'], 'last_date': wiki['last_edit']['date']}
                                for wiki in wikis
                                if 'first_edit' in wiki and 'last_edit' in wiki}
    return jsonify(time_spans)



@server_bp.route('/app/')
def redirect_app_to_classic():
    print('Redirecting user from old endpoint "/app" to /classic/app...')
    return flask.redirect('/classic/app/?{}'.format(bytes.decode(request.query_string)), code=302)


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


@server_bp.route('/lib/<dep>', defaults={'path': ''})
@server_bp.route('/lib/<path:path>/<dep>')
def serve_lib_in_dev(path, dep):
    path = os.path.join('lib/', path)
    return flask.send_from_directory(path, dep)



