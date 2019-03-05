#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
   app.py

   Descp: Code related to the Dash app.

   Created on: 23-oct-2017

   Copyright 2017-2019 Youssef 'FRYoussef' El Faqir El Rhazoui <f.r.youssef@hotmail.com>
   Copyright 2017-2019 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

# built-in imports
import os
import json
import time
from datetime import datetime
from warnings import warn

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
from flask import current_app

# imports for download feature
from fs.tempfs import TempFS
from flask import send_file, request
from urllib.parse import parse_qs
from codecs import decode

# Local imports:
import networks.interface
from version import __version__
import cache

# production or development (DEBUG) flag:
global debug;
debug = True if os.environ.get('FLASK_ENV') == 'development' else False

######### GLOBAL VARIABLES #########

# get csv data location (data/ by default)
global data_dir;
data_dir = os.getenv('WIKICHRON_DATA_DIR', 'data')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', # dash stylesheet
                        'https://use.fontawesome.com/releases/v5.0.9/css/all.css',  # fontawesome css
]

# list of js files to import from the app (either local or remote)
to_import_js = []

if debug:
    print('=> You are in DEBUG MODE <=')

else: # load piwik only in production:
    to_import_js.append('js/piwik.js')


def get_available_wikis(data_dir):
    wikis_json_file = open(os.path.join(data_dir, 'wikis.json'))
    wikis = json.load(wikis_json_file)
    return wikis


# other global variables:

available_networks = networks.interface.get_available_networks()
available_wikis = get_available_wikis(data_dir)
available_wikis_dict = {wiki['url']: wiki for wiki in available_wikis}
selection_params = {'wikis', 'network', 'lower_bound', 'upper_bound'}

######### AUX FUNCTION DEFINITIONS #########

# meta tags definition
def define_meta_tags(hostname, assets_url_path):
    meta_tags = [
        {
            'name': 'author',
            'content': "Abel 'Akronix' Serrano Juste"
        },
        {
            'name': 'description',
            'content': 'WikiChron Networks is a web tool for the analysis and visualization of different networks within wiki online communities'
        },
        {
            'name': 'og:title',
            'content': 'WikiChron - Networks'
        },
        {
            'name': 'og:description',
            'content': 'WikiChron Networks is a web tool for the visualization of networks within wikis'
        },
        {
            'name': 'og:url',
            'content': hostname
        },
        {
            'name': 'og:image',
            'content': '{}/wikichron_networks_logo.png'.format(assets_url_path)
        },
        {
            'name': 'og:image:width',
            'content': '600'
        },
        {
            'name': 'twitter:title',
            'content': 'WikiChron - Networks'
        },
    ]
    return meta_tags


######### BEGIN CODE ###########################################################


#--------- AUX FUNCS ----------------------------------------------------------#
def get_network_name_from_code(network_code):
    for nw in available_networks:
        if nw.CODE == network_code:
            return nw.NAME
    return None


def extract_wikis_from_selection_dict(selection):
    wikis = [ available_wikis_dict[wiki_url] for wiki_url in selection['wikis'] ]
    return (wikis)


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

            html.Div(id='side-bar-root', className='side-bar-cn'),
            html.Div(id='main-root', style={'flex': 'auto'}),
            html.Div(id='sidebar-selection', style={'display': 'none'}),
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
    assets_url_path = os.path.join(current_app.config['DASH_BASE_PATHNAME'],
                                    'assets')
    return html.Div(id='welcome-container',
            className='container',
            children=[
                html.Div(html.Img(src='{}/network-graph.svg'.format(assets_url_path))),
                html.H2([
                        html.Span('Welcome to '),
                        html.Span(
                            html.Img(src='{}/tipo-logo-networks.svg'.format(assets_url_path)),
                        ),
                    ],
                    style = {'display': 'flex'}
                ),
                html.Center([
                    html.P('Select one wiki and one network type from the sidebar on the left and press "generate" to start.',
                        style={'font-size': 'large'}),
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
            if selection.get('wikis') and selection.get('network'):

                (wikis) = extract_wikis_from_selection_dict(selection)

                network = {}
                network['code'] = selection['network']
                network['name'] = get_network_name_from_code(network['code'])

                return main.generate_main_content(wikis, network, query_string)


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

        # change value for network selection from a list to a single string
        #  since user can select only one network at a time
        if 'network' in selection:
            selection['network'] = selection['network'][0]

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

                # change value for network selection from a list to a single string
                # (first network we got of the query string),
                # since user can select only one network at a time
                pre_selected_network = selection['network'][0] if 'network' in selection else None

                return side_bar.generate_side_bar(available_wikis, available_networks,
                                                    pre_selected_wikis, pre_selected_network)

            else: # if app hasn't loaded the path yet, wait to load sidebar later
                return None;

        else:
            raise PreventUpdate("Sidebar already generated! sidebar must be generated only once");

    return


#--------- /download/ endpoint ------------------------------------------------#


def start_download_data_server(app):

    def is_valid(selection):
        # check empty query string
        if not selection:
            return False
        # check we have at least one metric and one wiki selected
        if not 'wikis' in selection or len(selection['wikis']) < 1 \
        or 'network' not in selection or len(selection['network']) < 1:
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

        wikis = extract_wikis_from_selection_dict(selection)
        network_code = selection['network'][0]
        lower_bound = ''
        upper_bound = ''
        if 'lower_bound' and 'upper_bound' in selection.keys():
            lower_bound = int(selection['lower_bound'][0])
            upper_bound = int(selection['upper_bound'][0])
            upper_bound = datetime.fromtimestamp(upper_bound).strftime("%Y-%m-%d %H:%M:%S")
            lower_bound = datetime.fromtimestamp(lower_bound).strftime("%Y-%m-%d %H:%M:%S")

        network = data_controller.get_network(wikis[0], network_code,
                lower_bound, upper_bound)

        tmp = TempFS()

        tmp.create('network.gml')
        path = tmp.getsyspath('/network.gml')

        network.write_gml(file = path)
        return send_file(filename_or_fp = path, as_attachment=True, attachment_filename='network.gml')

    return


#--------- APP CREATION FUNCS -------------------------------------------------#

def create_dash_app(server):
    # load config
    wikichron_base_pathname = server.config['DASH_BASE_PATHNAME'];
    assets_url_path = os.path.join(wikichron_base_pathname, 'assets')
    assets_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'resources', 'assets');
    meta_tags = define_meta_tags(server.config['APP_HOSTNAME'], assets_url_path)

    print('Creating new Dash instance...')
    app = dash.Dash(__name__,
                    server = server,
                    meta_tags = meta_tags,
                    external_stylesheets = external_stylesheets,
                    url_base_pathname = wikichron_base_pathname,
                    assets_folder = assets_folder)
    app.title = 'WikiChron - Networks'
    app.config['suppress_callback_exceptions'] = True

    # uncoment for offline serving of css:
    #~ app.css.config.serve_locally = True

    # uncoment for offline serving of js:
    #~ app.scripts.config.serve_locally = True

    # skeleton.css: (Already included in dash stylesheet)
    #~ app.css.append_css({"external_url": "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css"})

    cache.set_up_cache(app, debug)
    global data_controller
    import data_controller

    return app


def _init_app_callbacks(app):
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
    _init_app_callbacks(app)

    # set app layout
    print('Setting up layout...')
    app.layout = html.Div([
        set_layout(),
        load_external_dash_libs_in_layout()
    ])
    app.layout.children += set_external_imports()

    start_download_data_server(app)

    print('¡¡¡¡ Welcome to WikiChron-networks ' + __version__ +' !!!!')
    print('Using version ' + dash.__version__ + ' of Dash.')
    print('Using version ' + dash_renderer.__version__ + ' of Dash renderer.')
    print('Using version ' + dcc.__version__ + ' of Dash Core Components.')
    print('Using version ' + gdc.__version__ + ' of Grasia Dash Components.')
    print('Using version ' + html.__version__ + ' of Dash Html Components.')

    return

