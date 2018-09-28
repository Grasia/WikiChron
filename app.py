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

# Dash framework imports
import dash
import dash_core_components as dcc
import grasia_dash_components as gdc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go

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
    os.environ['WIKICHRON_DATA_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
data_dir = os.environ['WIKICHRON_DATA_DIR']

# global app config
port = 8880;
wikichron_base_pathname = '/app/';

#~ global app;
app = dash.Dash('WikiChron', url_base_pathname=wikichron_base_pathname)
app.title = 'WikiChron'
server = app.server
app.config['suppress_callback_exceptions'] = True
app.scripts.config.serve_locally = True

cache.set_up_cache(app, debug)

# js files being serve by this server:
local_available_js = ['side_bar.js', 'piwik.js']

# list of js files to import from the app (either local or remote)
to_import_js = []



# Redirects index to /app
@app.server.route('/')
def redirect_index_to_app():
    return flask.redirect(wikichron_base_pathname, code=302)


if debug:
    print('=> You are in DEBUG MODE <=')

else:
    to_import_js.append('js/piwik.js')
    #~ app.scripts.append_script({
        #~ "external_url": "js/piwik.js",
        #~ "external_url": "js/app.js",
        # Equivalent online (codepen:)
        #"external_url": "https://codepen.io/akronix/pen/rpQgqQ.js"
    #~ })

#~ app.css.config.serve_locally = True

#~ app.css.append_css({'external_url': 'dash.css'})
#~ app.css.append_css({'external_url': 'app.css'})
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
app.css.append_css({"external_url": "https://codepen.io/akronix/pen/BJNgRB.css"})
app.css.append_css({"external_url": "https://use.fontawesome.com/releases/v5.0.9/css/all.css"})

#~ app.css.append_css({"external_url": "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css"})

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


def set_up_app(app):
    app.layout = html.Div([
        set_layout(),
    ])
    app.layout.children += set_external_imports()
    return


def set_external_imports():
    if not to_import_js:
        return [gdc.Import()]
    else:
        return [gdc.Import(src=src) for src in to_import_js];


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


def init_app_callbacks():


    @app.callback(Output('main-root', 'children'),
    [Input('sidebar-selection', 'children')])
    def load_main_graphs(selection_json):
        if debug:
            print('load_main_graphs: This is the selection: {}'.format(selection_json))

        if selection_json:
            selection = json.loads(selection_json)

            if selection.get('wikis') and selection.get('metrics'):
                wikis = [ available_wikis_dict[wiki_url] for wiki_url in selection['wikis'] ]
                metrics = [ available_metrics_dict[metric] for metric in selection['metrics'] ]
                relative_time = len(wikis) > 1

                return main.generate_main_content(wikis, metrics, relative_time)


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


def start_css_server():
    # Add a static styles route that serves css from desktop
    # Be *very* careful here - you don't want to serve arbitrary files
    # from your computer or server
    static_css_route = '/styles/'
    css_directory = os.path.dirname(os.path.realpath(__file__)) + static_css_route
    stylesheets = ['app.css']

    @app.server.route('{}<css_path>.css'.format(static_css_route))
    def serve_stylesheet(css_path):
        css_name = '{}.css'.format(css_path)
        if css_name not in stylesheets:
            raise Exception(
                '"{}" is excluded from the allowed static files'.format(
                    css_path
                )
            )
        print ('Returning: {}'.format(css_name))
        return flask.send_from_directory(css_directory, css_name)


    for stylesheet in stylesheets:
        app.css.append_css({"external_url": "/styles/{}".format(stylesheet)})
    return


print('¡¡¡¡ Welcome to WikiChron ' + __version__ +' !!!!')
print('Using version ' + dcc.__version__ + ' of Dash Core Components.')
print('Using version ' + gdc.__version__ + ' of Grasia Dash Components.')
print('Using version ' + html.__version__ + ' of Dash Html Components.')

time_start_app = time.perf_counter()

# start auxiliar servers:
start_css_server()
start_js_server()

# Layout of the app:
# imports
#~ from tabs_bar import generate_tabs_bar
import side_bar
import main

# set layout and import js
set_up_app(app)

# bind callbacks
side_bar.bind_callbacks(app)
main.bind_callbacks(app)
init_app_callbacks()

time_loaded_app = time.perf_counter() - time_start_app
print(' * [Timing] Loading the app: {} seconds'.format(time_loaded_app) )

if __name__ == '__main__':
    app.run_server(debug=debug, port=port)
