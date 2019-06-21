#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
   app.py

   Descp:

   Created on: 23-oct-2017

   Copyright 2017-2018 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""
# Python built-in imports
import flask
import glob
import os
import json
import glob
import time
from warnings import warn
from urllib.parse import parse_qs, urljoin
from codecs import decode
from io import BytesIO
import zipfile

# Dash framework imports
import dash
import dash_core_components as dcc
import grasia_dash_components as gdc
import dash_renderer
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
import sd_material_ui

# Other external imports:
from flask import request, current_app
import pandas as pd

# Local imports:
from .utils import get_mode_config
from .metrics import interface as interface
from . import cache
from . import data_controller

# production or development (DEBUG) flag:
global debug
debug = True if os.environ.get('FLASK_ENV') == 'development' else False


######### GLOBAL VARIABLES #########

# list of js files to import from the app (either local or remote)
to_import_js = []

if debug:
    print('=> You are in DEBUG MODE <=')

else: # load piwik only in production:
    to_import_js.append('/js/piwik.js')

# other global variables:
global selection_params
selection_params = {'wikis', 'metrics', 'lower_bound', 'upper_bound'}

# The folowing ones will be set later on
global available_metrics
global available_metrics_dict
global available_wikis
global available_wikis_dict
global side_bar
global main


######### BEGIN CODE ###########################################################


#--------- AUX FUNCS ----------------------------------------------------------#


# meta tags definition
def define_meta_tags(hostname, assets_url_path):
    meta_tags = [
        {
            'name': 'author',
            'content': "Abel 'Akronix' Serrano Juste"
        },
        {
            'name': 'description',
            'content': 'WikiChron is a web tool for the analysis and visualization of the evolution of wiki online communities'
        },
        {
            'name': 'og:title',
            'content': 'WikiChron - Compare'
        },
        {
            'name': 'og:description',
            'content': 'WikiChron is a web tool for the visualization of wikis evolution'
        },
        {
            'name': 'og:url',
            'content': hostname
        },
        {
            'name': 'og:image',
            'content': '{}/logo_wikichron.png'.format(assets_url_path)
        },
        {
            'name': 'og:image:width',
            'content': '600'
        },
        {
            'name': 'twitter:title',
            'content': 'WikiChron - Compare'
        },
    ]
    return meta_tags


def extract_wikis_and_metrics_from_selection_dict(selection):
    wikis = [ available_wikis_dict[wiki_url] for wiki_url in selection['wikis'] ]
    metrics = [ available_metrics_dict[metric] for metric in selection['metrics'] ]
    return (wikis, metrics)


def set_external_imports():
    if not to_import_js:
        return [gdc.Import()]
    else:
        return [gdc.Import(src=src) for src in to_import_js]


#--------- LAYOUT ----------------------------------------------------------#

def set_layout(has_side_bar):

    side_bar = [html.Div(id='side-bar-root', className='side-bar-cn')] if has_side_bar else []

    return html.Div(id='app-layout',
        style={'display': 'flex'},
        children=[
            dcc.Location(id='url', refresh=False),
            html.Div(id='on-load', style={'display': 'none'})
            ] + side_bar + [
            html.Div(id='main-root'),
            html.Div(id='sidebar-selection', style={'display': 'none'}),
            html.Div(id='test', style={'display': 'none'})
        ]
    )


def load_external_dash_libs_in_layout():
    return html.Div(id='external-dash-libs',
        style={'display': 'none'},
        children=[
            sd_material_ui.Divider()
        ]
    )


def generate_welcome_page():
    mode_config = get_mode_config(current_app)
    assets_url_path = os.path.join(mode_config['DASH_STATIC_PATHNAME'],
                                    'assets')
    return html.Div(id='welcome-container',
            className='container',
            children=[
                html.Div(html.Img(src='{}/line-graph.svg'.format(assets_url_path))),
                html.H2([
                    'Welcome to ',
                    html.Span(html.Img(src='{}/tipo-logo.svg'.format(assets_url_path)),
                        style={'vertical-align': 'text-bottom'}
                    )]
                ),
                html.Center([
                    html.P('Select some wikis and metrics from the sidebar on the left and press compare to start.',
                        style={'font-size': 'large'}),
                    html.P(['You can read more info about WikiChron basic concepts and assumptions ',
                            html.A('here',
                                    href='https://github.com/Grasia/WikiChron/wiki/Basic-concepts',
                                    target='_blank'),
                            '.'],
                        style={'font-size': 'large'})
                ])
            ]
    )


#--------- CALLBACKS ----------------------------------------------------------#

def app_bind_callbacks(app):


    @app.callback(
        Output('main-root', 'children'),
        [Input('sidebar-selection', 'children')],
        [State('url', 'search')]
    )
    def load_main_graphs(selection_json, query_string):
        if debug:
            print('load_main_graphs: This is the selection: {}'.format(selection_json))

        if selection_json:
            selection = json.loads(selection_json)

            if selection.get('wikis') and selection.get('metrics'):

                (wikis, metrics) = extract_wikis_and_metrics_from_selection_dict(selection)

                relative_time = len(wikis) > 1

                return main.generate_main_content(wikis, metrics,
                                                relative_time, query_string)


        print('There is not a valid wikis & metrics tuple selection yet for plotting any graph')
        return generate_welcome_page()


    @app.callback(
        Output('sidebar-selection', 'children'),
        [Input('url', 'search')]
    )
    def write_query_string_in_hidden_selection_div(query_string):

        #~ if not (query_string): # check query string is not empty
            #~ return None

        # Attention! query_string includes heading ? symbol
        query_string_dict = parse_qs(query_string[1:])

        # get only the parameters we are interested in for the side_bar selection
        selection = { param: query_string_dict[param] for param in set(query_string_dict.keys()) & selection_params }

        if debug:
            print('selection to write in query string: {}'.format(selection))
        return (json.dumps(selection))


    @app.callback(Output('side-bar-root', 'children'),
        [Input('url', 'pathname')],
        [State('side-bar-root', 'children'),
        State('url', 'search')],
    )
    def generate_side_bar_onload(pathname, sidebar, query_string):

        if pathname:
            if debug:
                print('--> Dash App Loaded!')
                print('\tAnd this is current path: {}'.format(pathname))

        if not sidebar:

            if pathname:

                # Attention! query_string includes heading ? symbol
                selection = parse_qs(query_string[1:])

                if debug:
                    print('generate_side_bar_onload: This is the selection: {}'.format(selection))

                # we might have selection of wikis and metrics in the query string,
                #  so sidebar should start with those selected.
                pre_selected_wikis   = selection['wikis'] if 'wikis' in selection else []
                pre_selected_metrics = selection['metrics'] if 'metrics' in selection else []

                return side_bar.generate_side_bar(available_wikis, available_metrics,
                                                    pre_selected_wikis, pre_selected_metrics)

            else: # if app hasn't loaded the path yet, wait to load sidebar later
                return None

        else:
            raise PreventUpdate("Sidebar already generated! sidebar must be generated only once")

    return


#--------- BEGIN AUX SERVERS --------------------------------------------------#


def start_download_data_server(app, download_pathname):

    def is_valid(selection):
        # check empty query string
        if not selection:
            return False
        # check we have at least one metric and one wiki selected
        if not 'wikis' in selection or len(selection['wikis']) < 1 \
        or 'metrics' not in selection or len(selection['metrics']) < 1:
            return False
        # everything OK
        else:
            return True

    @app.server.route(download_pathname) #TOMOVEUP
    def download_data_classic():

        selection = parse_qs(decode(request.query_string))
        print ('Received this selection to download: {}'.format(selection))
        if not is_valid(selection):
            return 'Nothing to download!'

        (wikis, metrics) = extract_wikis_and_metrics_from_selection_dict(selection)

        data = data_controller.load_and_compute_data(wikis, metrics)

        # output in-memory zip file
        in_memory_zip = BytesIO()
        zipfile_ob = zipfile.ZipFile(in_memory_zip, mode='w',
                                    compression=zipfile.ZIP_DEFLATED)

        # For each wiki, create a DataFrame and add a column for the data of
        #   each metric.
        # Then, generate a csv for that DataFrame and append it to the output zip file
        # Remember this is the structure of data: data[metric][wiki]
        for wiki_idx in range(len(data[0])):

            # These two following lines are equivalent to the other next 3 lines
            #   but they are, probably, more difficult to understand and
            #  to maintain, although probably more pandas-ish:
            #~ metrics_data_for_this_wiki = [metric[wiki_idx] for metric in data ]
            #~ wiki_df = pd.concat(metrics_data_for_this_wiki, axis=1)

            wiki_df = pd.DataFrame()
            for metric in data:
                # assign the name of the metric as the name of the column for its data:
                wiki_df[metric[wiki_idx].name] = metric[wiki_idx]

            csv_str = wiki_df.to_csv()
            # append dataframe csv to zip file with name of the wiki:
            zipfile_ob.writestr('{}.csv'.format(wikis[wiki_idx]['name']), csv_str)

        # testing zip format and integrity
        error = zipfile_ob.testzip()
        if error is None:
            zipfile_ob.close()
            in_memory_zip.seek(0) # move ByteIO cursor to the start
            return flask.send_file(in_memory_zip, as_attachment=True,
                        attachment_filename='computed_data.zip',
                        mimetype='application/zip')
        else:
            zipfile_ob.close()
            raise Exeption('There was an error compressing the data in a zip file: {}'.format(error))

    return

#--------- APP CREATION FUNCS -------------------------------------------------#

def create_dash_app(server):
    # load config
    config = get_mode_config(server)
    wikichron_base_pathname = config['DASH_BASE_PATHNAME']
    path_to_serve_assets = config['DASH_STATIC_FOLDER']
    assets_url_path = os.path.join(config['DASH_STATIC_PATHNAME'], 'assets')
    assets_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                path_to_serve_assets)

    schema_and_hostname = f'{server.config["PREFERRED_URL_SCHEME"]}://{server.config["APP_HOSTNAME"]}'
    meta_tags = define_meta_tags(schema_and_hostname, assets_url_path)

    print('Creating new Dash instance...')
    app = dash.Dash(__name__,
                    server = server,
                    meta_tags = meta_tags,
                    url_base_pathname = wikichron_base_pathname,
                    assets_url_path = path_to_serve_assets,
                    assets_folder = assets_folder)
    app.title = 'WikiChron - Compare'
    app.config['suppress_callback_exceptions'] = True

    if debug: # In development use offline serving of deps
        app.css.config.serve_locally = True
        app.scripts.config.serve_locally = True


    app_cache = cache.set_up_cache(app, debug)
    data_controller.set_cache(app_cache)

    return app


def _init_global_vars():
    global available_wikis
    global available_wikis_dict
    global available_metrics
    global available_metrics_dict

    available_metrics = interface.get_available_metrics()
    available_metrics_dict = interface.get_available_metrics_dict()
    available_wikis = data_controller.get_available_wikis()
    available_wikis_dict = {wiki['domain']: wiki for wiki in available_wikis}


def _init_app_callbacks(app):
    global side_bar
    from . import side_bar #TOREMOVE (Probably)
    global main
    from . import main

    app_bind_callbacks(app)
    side_bar.bind_callbacks(app)
    main.bind_callbacks(app)
    return


def set_up_app(app):
    # init global vars needed for building UI app components
    _init_global_vars()

    # bind callbacks
    print('Binding callbacks...')
    _init_app_callbacks(app)

    # load Flask config
    server_config = app.server.config
    # load Dash config
    mode_config = get_mode_config(app.server)

    # set app layout
    print('Setting up layout...')
    has_side_bar = mode_config['DASH_STANDALONE']
    app.layout = html.Div([
        set_layout(has_side_bar),
        load_external_dash_libs_in_layout()
    ])
    app.layout.children += set_external_imports()

    start_download_data_server(app, mode_config['DASH_DOWNLOAD_PATHNAME'])

    print('¡¡¡¡ Welcome to WikiChron ' + server_config['VERSION'] +' !!!!')
    print('Using version ' + dash.__version__ + ' of Dash.')
    print('Using version ' + dash_renderer.__version__ + ' of Dash renderer.')
    print('Using version ' + dcc.__version__ + ' of Dash Core Components.')
    print('Using version ' + gdc.__version__ + ' of Grasia Dash Components.')
    print('Using version ' + html.__version__ + ' of Dash Html Components.')

    return

