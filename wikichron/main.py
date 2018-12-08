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

import dash
import dash_cytoscape
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
import grasia_dash_components as gdc
import sd_material_ui

# Local imports:
import lib.interface as lib
from cache import cache

global debug
debug = True #if os.environ.get('FLASK_ENV') == 'development' else False

# get csv data location (data/ by default)
global data_dir;
data_dir = os.getenv('WIKICHRON_DATA_DIR', 'data')



def clean_up_bot_activity(df, wiki):
    if 'botsids' in wiki:
        return lib.remove_bots_activity(df, wiki['botsids'])
    else:
        warn("Warning: Missing information of bots ids. Note that graphs can be polluted of non-human activity.")
    return df


def get_dataframe_from_csv(csv):
    """ Read and parse a csv and return the corresponding pandas dataframe"""
    print('Loading csv for ' + csv)
    time_start_loading_one_csv = time.perf_counter()
    df = pd.read_csv(os.path.join(data_dir, csv),
                    delimiter=';', quotechar='|',
                    index_col=False)
    df['timestamp']=pd.to_datetime(df['timestamp'],format='%Y-%m-%dT%H:%M:%SZ')
    #~ df.set_index(df['timestamp'], inplace=True) # generate a datetime index
    #~ print(df.info())
    print('!!Loaded csv for ' + csv)
    time_end_loading_one_csv = time.perf_counter() - time_start_loading_one_csv
    print(' * [Timing] Loading {} : {} seconds'
                    .format(csv, time_end_loading_one_csv))
    df.index.name = csv
    return df


@cache.memoize(timeout=3600)
def load_data(wiki):
    df = get_dataframe_from_csv(wiki['data'])
    lib.prepare_data(df)
    df = clean_up_bot_activity(df, wiki)
    return df

def to_cytoscape_dict(di_nodes, di_edges):
    """
    Transform an input dict to cytoscape dict

    Parameters:
        -di_nodes: A dict with nodes loaded with "generate_network"
        -di_edges: A dict with edges loaded with "generate_network"

    Return:
        A dict with the cytoscape structure of nodes and edges
    """
    network = []
    for key, val in di_nodes.items():
        network.append({
            'data': {
                'id': key,
                'label': val['label'],
                'num_edits': val['num_edits'],
                'last_edit': val['last_edit']
            }
        })
    for key, val in di_edges.items():
        network.append({
            'data': {
                'id': key,
                'source': val['source'],
                'target': val['target'],
                'weight': val['weight']
            }
        })
    # print(network)
    # print('aristas : {}\nnodos: {}'.format(len(di_edges), len(di_nodes)))
    return network

def generate_network(dataframe):
    """
    Generates a dict with the network

    Parameters:
        -dataframe: A pandas object with the wiki info

    Return: A tuple (nodes, edges) with the network representation
    """
    di_nodes = {}
    di_edges = {}
    user_per_page = {}

    for index, r in dataframe.iterrows():
        if r['contributor_name'] == 'Anonymous':
            continue

        # Nodes
        if not r['contributor_id'] in di_nodes:
            di_nodes[r['contributor_id']] = {}
            di_nodes[r['contributor_id']]['label'] = \
                                    r['contributor_name']
            di_nodes[r['contributor_id']]['num_edits'] = 0

        di_nodes[r['contributor_id']]['num_edits'] += 1
        di_nodes[r['contributor_id']]['last_edit'] = r['timestamp']

        # A page gets serveral contributors
        if not r['page_id'] in user_per_page:
            user_per_page[r['page_id']] = {r['contributor_id']}
        else:
            user_per_page[r['page_id']].add(r['contributor_id'])

    # Edges
    for k, p in user_per_page.items():
        aux = list(p)
        for i in range(len(aux)):
            for j in range(i+1, len(aux)):
                key1 = '{}{}'.format(aux[i],aux[j])
                key2 = '{}{}'.format(aux[j],aux[i])
                if key1 in di_edges:
                    di_edges[key1]['weight'] += 1
                    continue
                if key2 in di_edges:
                    di_edges[key2]['weight'] += 1
                    continue
                di_edges[key1] = {}
                di_edges[key1]['source'] = aux[i]
                di_edges[key1]['target'] = aux[j]
                di_edges[key1]['weight'] = 1

    return (di_nodes, di_edges)



@cache.memoize()
def load_and_compute_data(wiki, _):

    # load data from csvs:
    time_start_loading_csvs = time.perf_counter()
    df = load_data(wiki)
    time_end_loading_csvs = time.perf_counter() - time_start_loading_csvs
    print(' * [Timing] Loading csvs : {} seconds'.format(time_end_loading_csvs) )

    # compute metric data:
    print(' * [Info] Starting calculations....')
    time_start_calculations = time.perf_counter()
    nodes, edges = generate_network(df)
    network = to_cytoscape_dict(nodes, edges)
    time_end_calculations = time.perf_counter() - time_start_calculations
    print(' * [Timing] Calculations : {} seconds'.format(time_end_calculations) )
    return network


def generate_main_content(wikis_arg, metrics_arg, relative_time_arg,
                            query_string, url_host):
    """
    @TODO: Quit unused args
    It generates the main content
    Parameters: 
            -wikis_arg: wikis to show, only used the first wiki
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
                    html.Span(
                        html.Img(src='/assets/logo_wikichron.svg'),
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

    def network():
        """
        Generates the network dashboard

        Return: An HTML object with the notwork dashboard
        """
        return html.Div(id='cytoscape', children=[
                dash_cytoscape.Cytoscape(
                    elements=[],
                    layout={
                    'name': 'cose'
                    },
                    style = {
                            'height': '100%',
                            'width': '100%',
                            'position': 'absolute'       
                    }
                )
            ]);

    if debug:
        print ('Generating main...')
    wikis = wikis_arg;
    relative_time = relative_time_arg;
    args_selection = json.dumps({"wikis": wikis, "relative_time": relative_time})

    return html.Div(id='main',
        className='control-text',
        style={'width': '100%'},
        children=[

            main_header(),

            html.Hr(),

            html.Div(id='graphs'),

            share_modal('{}/app/{}'.format(url_host, query_string),
                        '{}/download/{}'.format(url_host, query_string)),

            html.Div(id='initial-selection', style={'display': 'none'}, 
                        children=args_selection),
            network(),
            html.Div(id='signal-data', style={'display': 'none'}),
            #html.Div(id='time-axis', style={'display': 'none'}),
            html.Div(id='ready', style={'display': 'none'})
        ]
    );

def bind_callbacks(app):

    @app.callback(
        Output('cytoscape', 'children'),
        [Input('initial-selection', 'children')]
    )
    def start_main(selection_json):
        # get wikis x metrics selection
        selection = json.loads(selection_json)
        wiki = selection['wikis'][0]

        print('--> Retrieving and computing data')
        print( '\t for the following wikis: {}'.format( wiki['name'] ))
        network = load_and_compute_data(wiki, None)
        print('<-- Done retrieving and computing data!')

        return dash_cytoscape.Cytoscape(
                    elements=network,
                    layout={
                    'name': 'concentric'
                    },
                    style = {
                            'height': '100%',
                            'width': '100%',
                            'position': 'absolute'       
                    }
                )


    # @app.callback(
    #     Output('ready', 'children'),
    #     [Input('signal-data', 'children')]
    # )
    # def ready_to_plot_networks(signal):
    #     #~ print (signal)
    #     if not signal:
    #         print('not ready!')
    #         return None
    #     if debug:
    #         print('Ready to plot network!')
    # return 'ready'


    # @app.callback(
    #     Output('cytoscape', 'children'),
    #     [Input('signal-data', 'children')],
    #     [State('initial-selection', 'children')]
    # )
    # def update_network(ready, selection_json):

    #     if not ready: # waiting for all parameters to be ready
    #         return
    #     selection = json.loads(selection_json)
    #     wiki = selection['wikis'][0]
    #     print('\n\n\n\n')
    #     nodes = load_and_compute_data(wiki, None)
    #     print(nodes)
    #     nodes = to_cytoscape_dict(nodes)
    #     print(nodes)

    #     return html.Div([
    #             dash_cytoscape.Cytoscape(
    #                 id='cytoscape',
    #                 elements=[
    #                     {'data': {'id': 'one', 'label': 'Node 1'}},
    #                     {'data': {'id': 'two', 'label': 'Node 2'}},
    #                     {'data': {'id': 'a', 'label': 'Node A'}},
    #                     {'data': {'source': 'one', 'target': 'two','label': 'Node 1 to 2'}},
    #                     {'data': {'source': 'one', 'target': 'a','label': 'Node 1 to a'}}
    #                 ],

    #                 layout={
    #                 'name': 'cose'
    #                 },
    #                 style = {
    #                         'height': '100%',
    #                         'width': '100%',
    #                         'position': 'absolute'       
    #                 }
    #             )
    #         ]);

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
