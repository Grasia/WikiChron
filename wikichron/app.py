#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
   app.py

   Descp:

   Created on: 23-oct-2017

   Copyright 2017-2018 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""
# built-in imports
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
from flask import request
import pandas as pd

# Local imports:
import lib.interface as lib
from version import __version__
import cache

# production or development (DEBUG) flag:
global debug;
debug = True if os.environ.get('FLASK_ENV') == 'development' else False

# get csv data location (data/ by default)
global data_dir;
if not 'WIKICHRON_DATA_DIR' in os.environ:
    os.environ['WIKICHRON_DATA_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')
data_dir = os.environ['WIKICHRON_DATA_DIR']

# global app config
APP_HOSTNAME = 'http://wikichron.science';
port = 8880;
wikichron_base_pathname = '/app/';
#~ assets_url_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets');
assets_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets');


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', # dash stylesheet
                        'https://use.fontawesome.com/releases/v5.0.9/css/all.css',  # fontawesome css
]


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
        'content': 'WikiChron'
    },
    {
        'name': 'og:description',
        'content': 'WikiChron is a web tool for the visualization of wikis evolution'
    },
    {
        'name': 'og:url',
        'content': 'http://wikichron.science/'
    },
    {
        'name': 'og:image',
        'content': '/assets/logo_wikichron.png'
    },
    {
        'name': 'twitter:title',
        'content': 'WikiChron'
    },
]

# js files being serve by this server:
local_available_js = ['side_bar.js', 'main.share_modal.js', 'piwik.js']

# list of js files to import from the app (either local or remote)
to_import_js = []

global app;

if debug:
    print('=> You are in DEBUG MODE <=')

else: # load piwik only in production:
    to_import_js.append('js/piwik.js')


#~ tabs = [
    #~ {'value': 1, 'icon': '/assets/white_graphic.svg'},
    #~ {'value': 2, 'icon': '/assets/white_graphic.svg'},
    #~ {'value': 3, 'icon': '/assets/white_graphic.svg'},
    #~ {'value': 4, 'icon': '/assets/white_graphic.svg'},
#~ ]


def get_available_wikis(data_dir):
    wikis_json_file = open(os.path.join(data_dir, 'wikis.json'))
    wikis = json.load(wikis_json_file)
    return wikis

# other global variables:

available_metrics = lib.get_available_metrics()
available_metrics_dict = lib.metrics_dict
available_wikis = get_available_wikis(data_dir)
available_wikis_dict = {wiki['url']: wiki for wiki in available_wikis}
selection_params = {'wikis', 'metrics'}


######### BEGIN CODE ###########################################################


#--------- AUX FUNCS ----------------------------------------------------------#

def extract_wikis_and_metrics_from_selection_dict(selection):
    wikis = [ available_wikis_dict[wiki_url] for wiki_url in selection['wikis'] ]
    metrics = [ available_metrics_dict[metric] for metric in selection['metrics'] ]
    return (wikis, metrics)


def set_external_imports():
    if not to_import_js:
        return [gdc.Import()]
    else:
        return [gdc.Import(src=src) for src in to_import_js];


#--------- LAYOUT ----------------------------------------------------------#

def set_layout():
    return html.Div(id='app-layout',
        style={'display': 'flex'},
        children=[
            dcc.Location(id='url', refresh=False),
            html.Div(id='on-load', style={'display': 'none'}),

            #~ generate_tabs_bar(tabs),
            #~ side_bar.generate_side_bar(available_wikis, available_metrics),
            html.Div(id='side-bar'),
            html.Div(id='main-root', style={'flex': 'auto'}),
            html.Div(id='sidebar-selection', style={'display': 'none'}),
            html.Div(id='test', style={'display': 'none'})
        ]
    );


def load_external_dash_libs_in_layout():
    return html.Div(id='external-dash-libs',
        style={'display': 'none'},
        children=[
            sd_material_ui.Divider()
        ]
    );


def generate_welcome_page():
    return html.Div(id='welcome-container',
            className='container',
            children=[
                html.Div(html.Img(src='/assets/line-graph.svg')),
                html.H2([
                    'Welcome to ',
                    html.Span(html.Img(src='/assets/tipo-logo.svg'),
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
                                                relative_time, query_string, APP_HOSTNAME)


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


    @app.callback(Output('side-bar', 'children'),
        [Input('url', 'pathname')],
        [State('side-bar', 'children'),
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
                return None;

        else:
            raise PreventUpdate("Sidebar already generated! sidebar must be generated only once");

    return


#--------- BEGIN AUX SERVERS --------------------------------------------------#

def start_redirection_server():
    # Redirects index to /app
    @app.server.route('/')
    def redirect_index_to_app():
        print('Redirecting user to {}...'.format(wikichron_base_pathname))
        return flask.redirect(wikichron_base_pathname, code=302)


# we want to load some js dnymically:
# from the side_bar generation (generated by a dash callback) using gdc.Import()
# So that's why we still need this function to serve the js files but don't load them
# automatically when the app is loaded, but when we want to do it.
# It might have a better solution, but let it _just work_
def start_js_server():
    static_js_route = 'js/'
    js_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                 static_js_route)

    server_js_route = urljoin(wikichron_base_pathname, static_js_route)

    @app.server.route(urljoin(server_js_route, '<js_path>.js'))
    def serve_local_js(js_path):
        js_name = '{}.js'.format(js_path)
        if js_name not in local_available_js:
            raise Exception(
                '"{}" is excluded from the allowed static files'.format(
                    js_path
                )
            )
        print ('Returning: {}'.format(js_name))
        return flask.send_from_directory(js_directory, js_name)

    return


def start_download_data_server():

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

    @app.server.route('/download/')
    def download_data_server():

        selection = parse_qs(decode(request.query_string))
        print ('Received this selection to download: {}'.format(selection))
        if not is_valid(selection):
            return 'Nothing to download!'

        (wikis, metrics) = extract_wikis_and_metrics_from_selection_dict(selection)

        data = main.load_and_compute_data(wikis, metrics)

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

def create_app():
    print('Creating new Dash instance...')
    global app;
    app = dash.Dash('WikiChron',
                    meta_tags = meta_tags,
                    external_stylesheets=external_stylesheets,
                    url_base_pathname=wikichron_base_pathname,
                    assets_folder=assets_folder)
    app.title = 'WikiChron'
    server = app.server
    app.config['suppress_callback_exceptions'] = True

    # uncoment for offline serving of css:
    #~ app.css.config.serve_locally = True

    # uncoment for offline serving of js:
    #~ app.scripts.config.serve_locally = True

    # skeleton.css: (Already included in dash stylesheet)
    #~ app.css.append_css({"external_url": "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css"})


    cache.set_up_cache(app, debug)

    return app


def init_app_callbacks(app):
    global side_bar
    import side_bar
    global main
    import main

    app_bind_callbacks(app)
    side_bar.bind_callbacks(app)
    main.bind_callbacks(app)
    return


def set_up_app(app):
    # bind callbacks
    print('Binding callbacks...')
    init_app_callbacks(app)

    # set app layout
    print('Setting up layout...')
    app.layout = html.Div([
        set_layout(),
        load_external_dash_libs_in_layout()
    ])
    app.layout.children += set_external_imports()
    return


def init_app(app):

    # start auxiliar servers:
    start_js_server()
    start_redirection_server()
    start_download_data_server()

    print('¡¡¡¡ Welcome to WikiChron ' + __version__ +' !!!!')
    print('Using version ' + dash.__version__ + ' of Dash.')
    print('Using version ' + dash_renderer.__version__ + ' of Dash renderer.')
    print('Using version ' + dcc.__version__ + ' of Dash Core Components.')
    print('Using version ' + gdc.__version__ + ' of Grasia Dash Components.')
    print('Using version ' + html.__version__ + ' of Dash Html Components.')

    return


def run(app):
    app.run_server(debug=debug, port=port)
    return


######### BEGIN MAIN ###########################################################

# create and config Dash instance
app = create_app()

# set layout, import startup js and bind callbacks
set_up_app(app)

# init auxiliar servers & deps
init_app(app)

print ('This is __name__: {}'.format(__name__))
if __name__ == '__main__':
    run(app)

else:
    server = app.server
