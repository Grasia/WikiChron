#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   main.py

   Descp: This script generates the main content of the site, this content includes
serveral interpretations of the network, which is generated from the wikis
data.

   Created on: 07-dec-2018

   Copyright 2017-2019 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
   Copyright 2017-2019 Youssef El Faqir El Rhazoui
"""

# Built-in imports
import os
import time
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
import data_handler
#from controls_sidebar import generate_controls_sidebar, bind_control_callbacks
from app import assets_url_path
from lib.cytoscape_decorator.Stylesheet import Stylesheet
from controls_sidebar_decorator.ControlsSidebar import ControlsSidebar
from controls_sidebar_decorator.factory_sidebar_decorator import factory_sidebar_decorator
from controls_sidebar_decorator.factory_sidebar_decorator import bind_controls_sidebar_callbacks

TIME_DIV = 60 * 60 * 24 * 30

global debug
debug = True if os.environ.get('FLASK_ENV') == 'development' else False


def generate_main_content(wikis_arg, network_type_arg, query_string, url_host):
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
                            html.Img(src='{}/wikichron_networks_logo.svg'.format(assets_url_path))
                        ],
                        id='tool-title'),
                    html.Div([
                        html.A(
                            html.Img(src='{}/share.svg'.format(assets_url_path)),
                            id='share-button',
                            className='icon',
                            title='Share current selection'
                        ),
                        html.A(
                            html.Img(src='{}/cloud_download.svg'.format(assets_url_path)),
                            href=href_download_button,
                            id='download-button',
                            target='_blank',
                            className='icon',
                            title='Download data'
                        ),
                        html.A(
                            html.Img(src='{}/documentation.svg'.format(assets_url_path)),
                            href='https://github.com/Grasia/WikiChron/wiki/',
                            target='_blank',
                            className='icon',
                            title='Documentation'
                        ),
                        html.A(
                            html.Img(src='{}/ico-github.svg'.format(assets_url_path)),
                            href='https://github.com/Grasia/WikiChron-networks',
                            target='_blank',
                            className='icon',
                            title='Github repo'
                        ),
                    ],
                    id='icons-bar')
            ])
        );

    def selection_title(selected_wiki, selected_network):
        selection_text = (f'You are viewing the {selected_network} network for wiki: {selected_wiki}')
        return html.Div([
            html.H3(selection_text, id = 'selection-title')],
            className = 'container'
        )

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

    def date_slider_control():
        return html.Div(id='date-slider-div', className='container',
                children=[
                    html.Span(id='slider-header',
                    children=[
                        html.Strong(
                            'Time interval (months):'),
                        html.Span(id='display-slider-selection')
                    ]),

                    html.Div(id='date-slider-container',
                        style={'height': '35px'},
                        children=[
                            dcc.Slider(
                                id='dates-slider'
                        )],
                    )
                ],
                style={'margin-top': '15px'}
                )

    def cytoscape_component():
        cytoscape = dash_cytoscape.Cytoscape(
                    id='cytoscape',
                    elements = [],
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
                        'height': '95vh',
                        'width': 'calc(100% - 300px)'
                    },
                    stylesheet = Stylesheet().cy_stylesheet
        )
        return html.Div(style={'display': 'flex'}, children=[cytoscape])

    if debug:
        print ('Generating main...')

    network_type_code = network_type_arg['code']
    args_selection = json.dumps({"wikis": wikis_arg, "network": network_type_code})

    selected_wiki_name = wikis_arg[0]['name']
    selected_network_name = network_type_arg['name']

    controls_sidebar = ControlsSidebar()
    sidebar_decorator = factory_sidebar_decorator(network_type_code, controls_sidebar)
    sidebar_decorator.add_all_sections()

    return html.Div(
            id='main',
            className='control-text',
            style={'width': '100%'},
            children=[

                #generate_controls_sidebar(),
                controls_sidebar.build(),

                main_header(),

                html.Hr(style={'margin-top': '0px'}),

                selection_title(selected_wiki_name, selected_network_name),

                date_slider_control(),

                html.Hr(style={'margin-bottom': '0px'}),

                share_modal('{}/app/{}'.format(url_host, query_string),
                            '{}/download/{}'.format(url_host, query_string)),

                html.Div(id='initial-selection', style={'display': 'none'},
                            children=args_selection),

                cytoscape_component(),

                html.Div(id='network-ready', style={'display': 'none'}),
                html.Div(id='signal-data', style={'display': 'none'}),
                html.Div(id='ready', style={'display': 'none'})
        ]);

def bind_callbacks(app):

    # Right sidebar callbacks
    #bind_control_callbacks(app)
    #########
    bind_controls_sidebar_callbacks('co_editing_network', app)
    #########

    @app.callback(
        Output('signal-data', 'value'),
        [Input('initial-selection', 'children')]
    )
    def start_main(selection_json):
        # get wikis x network selection
        selection = json.loads(selection_json)
        wiki = selection['wikis'][0]
        network_code = selection['network']
        print('--> Retrieving and computing data')
        print( '\t for the following wiki: {}'.format( wiki['url'] ))
        print( '\trepresented as this network: {}'.format( network_code ))
        network = data_handler.load_and_compute_data(wiki, network_code)
        print('<-- Done retrieving and computing data!')
        return True


    @app.callback(
        Output('ready', 'value'),
        [Input('signal-data', 'value'),
        Input('dates-slider', 'value')]
    )
    def ready_to_plot_networks(*args):
        #print (args)
        if not all(args):
            print('not ready!')
            return False
        if debug:
            print('Ready to plot network!')
        return True


    @app.callback(
        Output('network-ready', 'value'),
        [Input('ready', 'value'),
        Input('calculate_page_rank', 'n_clicks'),
        Input('calculate_communities', 'n_clicks')],
        [State('initial-selection', 'children'),
        State('date-slider-container', 'children'),
        State('network-ready', 'value')]
    )
    def update_network(ready, pr_clicks, com_clicks, selection_json, slider, cy_network):
        if not ready:
            return None

        # get network instance from selection
        selection = json.loads(selection_json)
        wiki = selection['wikis'][0]
        network_code = selection['network']


        if not slider['props']['value'] == slider['props']['max']:
            print(' * [Info] Starting time filter....')
            time_start_calculations = time.perf_counter()

            t_to_filter = cy_network['oldest_user'] + slider['props']['value'] * TIME_DIV
            t_to_filter = datetime.fromtimestamp(t_to_filter)\
                .strftime("%Y-%m-%d %H:%M:%S")

            network = data_handler.load_and_compute_data(wiki, network_code, t_to_filter)
            #network = network.filter_by_time(origin + slider['props']['value']
            # * TIME_DIV)

            time_end_calculations = time.perf_counter() - time_start_calculations
            print(' * [Timing] Filter : {} seconds'.format(time_end_calculations))

        else:
            print(' * [Info] Printing the entire network....')
            network = data_handler.load_and_compute_data(wiki, network_code)

        if pr_clicks and pr_clicks % 2 == 1:
            network.calculate_page_rank()

        if com_clicks and com_clicks % 2 == 1:
            network.calculate_communities()

        return network.to_cytoscape_dict()

    @app.callback(
        Output('cytoscape', 'elements'),
        [Input('network-ready', 'value')]
    )
    def add_network_elements(cy_network):
        return cy_network['network'] if cy_network else []


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


    @app.callback(
        Output('date-slider-container', 'children'),
        [Input('signal-data', 'value')],
        [State('initial-selection', 'children')]
    )
    def update_slider(signal, selection_json):
        if not signal:
            return dcc.Slider(id='dates-slider')

         # get network instance from selection
        selection = json.loads(selection_json)
        wiki = selection['wikis'][0]
        network_code = selection['network']
        network = data_handler.load_and_compute_data(wiki, network_code)

        origin = int(datetime.strptime(str(network.oldest_user),
            "%Y-%m-%d %H:%M:%S").strftime('%s'))
        end = int(datetime.strptime(str(network.newest_user),
            "%Y-%m-%d %H:%M:%S").strftime('%s'))

        time_gap = end - origin
        max_time = time_gap // TIME_DIV

        #~ max_number_of_marks = 11
        if max_time < 12:
            step_for_marks = 1
        elif max_time < 33:
            step_for_marks = 3
        elif max_time < 66:
            step_for_marks = 6
        elif max_time < 121:
            step_for_marks = 12
        elif max_time < 264:
            step_for_marks = 24
        else:
            step_for_marks = 36

        range_slider_marks = {i: datetime.fromtimestamp(origin
         + i * TIME_DIV).strftime('%b %Y') for i in range(1,
         max_time-step_for_marks, step_for_marks)}

        range_slider_marks[max_time] = datetime.fromtimestamp(
        origin + max_time * TIME_DIV).strftime('%b %Y')

        return  dcc.Slider(
                    id='dates-slider',
                    min=1,
                    max=max_time,
                    step=1,
                    value=max_time,
                    marks=range_slider_marks
                )

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

    app.layout = generate_main_content(wikis, metrics)

    bind_callbacks(app)

    app.run_server(debug=debug, port=8053)
