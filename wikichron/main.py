#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script generates the main content of the site, this content includes
serveral interpretations of the network, which is generated from the wikis
data.

"""
#
# Author: Youssef El Faqir El Rhazoui
# Based on Abel 'Akronix' Serrano Juste <akronix5@gmail.com> code
# Date: 07/12/2018
# Distributed under the terms of the GPLv3 license.
#

import os
import time
from warnings import warn
import json
from datetime import datetime
import dash
import dash_cytoscape
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import grasia_dash_components as gdc
import sd_material_ui

# Local imports:
import lib.interface as lib
from cache import cache
from lib.networks.types.CoEditingNetwork import CoEditingNetwork

global debug
debug = True if os.environ.get('FLASK_ENV') == 'development' else False

# get csv data location (data/ by default)
global data_dir;
data_dir = os.getenv('WIKICHRON_DATA_DIR', 'data')


def extract_network_obj_from_network_code(selected_network_code):
    if selected_network_code:
        return CoEditingNetwork()
    else:
        raise Exception("Something went bad. Missing network type selection.")


@cache.memoize(timeout=3600)
def load_data(wiki):
    df = lib.get_dataframe_from_csv(wiki['data'])
    lib.prepare_data(df)
    df = lib.clean_up_bot_activity(df, wiki)
    return df



@cache.memoize()
def load_and_compute_data(wiki, network_type):
    """
    Parameters
        - wiki: Related info about the wiki selected.
        - network_type: network selected. It is an instance of BaseNetwork.
    Return: Data representing the network.
    """

    # load data from csvs:
    time_start_loading_csvs = time.perf_counter()
    df = load_data(wiki)
    time_end_loading_csvs = time.perf_counter() - time_start_loading_csvs
    print(' * [Timing] Loading csvs : {} seconds'.format(time_end_loading_csvs) )

    # generate network:
    print(' * [Info] Starting calculations....')
    time_start_calculations = time.perf_counter()
    network_type.generate_from_pandas(data=df)
    #network_type = network_type.filter_by_timestamp("2011-04-07 02:05:56")
    di_net = network_type.to_cytoscape_dict()
    time_end_calculations = time.perf_counter() - time_start_calculations
    print(' * [Timing] Calculations : {} seconds'.format(time_end_calculations) )
    return di_net


def generate_main_content(wikis_arg, network_type_arg, relative_time_arg,
                            query_string, url_host):
    """
    It generates the main content
    Parameters:
        -wikis_arg: wikis to show, only used the first wiki
        -network_type_arg, type of network to generate
        -query_string: string to share/download
        -url_host: url to share/download
        -others: are not used

    Return: An HTML object with the main content
    """

    def main_header():
        """
        Generates the main header

        Return: An HTML object with the header content
        """
        href_download_button = '/download/{}'.format(query_string)
        return (html.Div(id='header',
                className='container',
                style={'display': 'flex', 'align-items': 'center', \
                        'justify-content': 'space-between'},
                children=[
                    html.Span([
                            html.Img(src='/assets/logo_wikichron.svg'),
                            html.Span('    '),
                            html.Strong(
                                html.Em('Networks'),
                                style={
                                    'marginLeft': '15px',
                                    'fontSize': 'large',
                                    'textDecoration': 'underline'
                                }
                            )
                        ],
                        id='tool-title'),
                    html.Div([
                        html.A(
                            html.Img(src='/assets/share.svg'),
                            id='share-button',
                            className='icon',
                            title='Share current selection'
                        ),
                        html.A(
                            html.Img(src='/assets/cloud_download.svg'),
                            href=href_download_button,
                            id='download-button',
                            target='_blank',
                            className='icon',
                            title='Download data'
                        ),
                        html.A(
                            html.Img(src='/assets/documentation.svg'),
                            href='https://github.com/Grasia/WikiChron/wiki/',
                            target='_blank',
                            className='icon',
                            title='Documentation'
                        ),
                        html.A(
                            html.Img(src='/assets/ico-github.svg'),
                            href='https://github.com/Grasia/WikiChron',
                            target='_blank',
                            className='icon',
                            title='Github repo'
                        ),
                    ],
                    id='icons-bar')
            ])
        );


    def share_modal(share_link, download_link):
        """
        Generates a window to share a link
        Parameters:
                -share_link: a link to share
                -download_link: a link to download

        Return: An HTML object with the window to share and download
        """
        return html.Div([
            sd_material_ui.Dialog(
                html.Div(children=[
                    html.H3('Share WikiChron with others or save your work!'),
                    html.P([
                      html.Strong('Link with your current selection:'),
                      html.Div(className='share-modal-link-and-button-cn', children=[
                        dcc.Input(value=share_link, id='share-link-input', readOnly=True, className='share-modal-input-cn', type='url'),
                        html.Div(className='tooltip', children=[
                          html.Button('Copy!', id='share-link', className='share-modal-button-cn'),
                        ])
                      ]),
                    ]),
                    html.P([
                      html.Strong('Link to download the data of your current selection:'),
                      html.Div(className='share-modal-link-and-button-cn', children=[
                        dcc.Input(value=download_link, id='share-download-input', readOnly=True, className='share-modal-input-cn', type='url'),
                        html.Div(className='tooltip', children=[
                          html.Button('Copy!', id='share-download', className='share-modal-button-cn'),
                        ])
                      ]),

                      html.Div([
                        html.Span('You can find more info about working with the data downloaded in '),
                        html.A('this page of our wiki.', href='https://github.com/Grasia/WikiChron/wiki/Downloading-and-working-with-the-data')
                        ],
                        className='share-modal-paragraph-info-cn'
                      )
                    ]),
                    gdc.Import(src='js/main.share_modal.js')
                    ],
                    id='share-dialog-inner-div'
                ),
                id='share-dialog',
                modal=False,
                open=False
            )
        ])


    if debug:
        print ('Generating main...')
    wikis = wikis_arg;
    relative_time = relative_time_arg;
    args_selection = json.dumps({"wikis": wikis, "relative_time": relative_time,
                                "network": network_type_arg})

    return html.Div(
        id='main',
        className='control-text',
        style={'width': '100%'},
        children=[

            main_header(),

            html.Hr(),

            share_modal('{}/app/{}'.format(url_host, query_string),
                        '{}/download/{}'.format(url_host, query_string)),

            html.Div(id='initial-selection', style={'display': 'none'},
                        children=args_selection),
            html.Div(id='cytoscape', children=[]),
            html.Div(id='signal-data', style={'display': 'none'}),
            html.Div(id='ready', style={'display': 'none'})
        ]);

def bind_callbacks(app):

    @app.callback(
        Output('signal-data', 'value'),
        [Input('initial-selection', 'children')]
    )
    def start_main(selection_json):
        # get wikis x network selection
        selection = json.loads(selection_json)
        wiki = selection['wikis'][0]
        network_type = extract_network_obj_from_network_code(selection['network'])

        print('--> Retrieving and computing data')
        print( '\t for the following wiki: {}'.format( wiki['name'] ))
        print( '\trepresented as this network: {}'.format( network_type.name ))
        load_and_compute_data(wiki, network_type)
        print('<-- Done retrieving and computing data!')

        return True


    @app.callback(
        Output('ready', 'value'),
        [Input('signal-data', 'value')]
    )
    def ready_to_plot_networks(signal):
        #print (signal)
        if not signal:
            print('not ready!')
            return False
        if debug:
            print('Ready to plot network!')
        return True


    @app.callback(
        Output('cytoscape', 'children'),
        [Input('ready', 'value'),
        Input('initial-selection', 'children')]
    )
    def show_network(ready, selection_json):
        if not ready: # waiting for all parameters to be ready
            return

        # get wikis x network selection
        selection = json.loads(selection_json)
        wiki = selection['wikis'][0]
        network_type = extract_network_obj_from_network_code(selection['network'])

        network = load_and_compute_data(wiki, network_type)

        return dash_cytoscape.Cytoscape(
                    elements = network['network'],
                    layout = {
                        'name': 'cose',
                        'idealEdgeLength': 100,
                        'nodeOverlap': 20,
                        'refresh': 20,
                        'fit': True,
                        'padding': 30,
                        'randomize': False,
                        'componentSpacing': 100,
                        'nodeRepulsion': 400000,
                        'edgeElasticity': 100,
                        'nestingFactor': 5,
                        'gravity': 80,
                        'numIter': 1000,
                        'initialTemp': 200,
                        'coolingFactor': 0.95,
                        'minTemp': 1.0
                    },
                    style = {
                        'height': '100%',
                        'width': '100%',
                        'position': 'absolute'
                    },
                    stylesheet = [{
                        'selector': 'node',
                        'style': {
                            'content': '',
                            'text-valign': 'center',
                            'color': 'white',
                            'text-outline-width': 2,
                            'background-color': 'mapData(first_edit, {}, {}, \
                                #004481, #B0BEC5)'.format(network['oldest_user'],
                                    network['newest_user']),
                            'text-outline-color': '#999',
                            'height': 'mapData(num_edits, {}, {}, 10, 60)'
                                .format(network['user_min_edits'],
                                    network['user_max_edits']),
                            'width': 'mapData(num_edits, {}, {}, 10, 60)'
                                .format(network['user_min_edits'],
                                    network['user_max_edits']),
                            'border-width': '1%',
                            'border-style': 'solid',
                            'border-color': 'black'
                        }
                    },
                    {
                        'selector': 'edge',
                        'style': {
                            "width": 'mapData(weight, {}, {}, 1, 10)'
                                .format(network['edge_min_weight'],
                                    network['edge_max_weight']),
                            'opacity': 'mapData(weight, {}, {}, 0.2, 1)'
                                .format(network['edge_min_weight'],
                                    network['edge_max_weight']),
                            'line-color': "#E53935",
                        }
                    }]
                )


    @app.callback(
        Output('share-dialog', 'open'),
        [Input('share-button', 'n_clicks')],
        [State('share-dialog', 'open')]
    )
    def show_share_modal(n_clicks: int, open_state: bool):
        if not n_clicks: # modal init closed
            return False
        elif n_clicks > 0 and not open_state: # opens if we click and `open` state is not open
            return True
        else: # otherwise, leave it closed.
            return False

        return # bind_callbacks


if __name__ == '__main__':

    data_dir = os.getenv('WIKICHRON_DATA_DIR', 'data')

    wikis = ['eslagunanegra_pages_full', 'cocktails', 'es.shamanking.wikia.com']

    available_metrics = lib.get_available_metrics()
    metrics = []
    metrics.append(available_metrics[0])
    metrics.append(available_metrics[1])

    app = dash.Dash()
    app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
    app.css.append_css({"external_url": "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css"})

    relative_time = False
    app.layout = generate_main_content(wikis, metrics, relative_time)

    bind_callbacks(app)

    app.run_server(debug=debug, port=8053)
