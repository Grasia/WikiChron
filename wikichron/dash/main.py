#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   main.py

   Descp: This script generates the main content of the site, this content includes
serveral interpretations of the network, which is generated from the wikis
data.

   Created on: 07-dec-2018

   Copyright 2017-2019 Youssef El Faqir El Rhazoui
   Copyright 2017-2019 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
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
from dash.exceptions import PreventUpdate
import grasia_dash_components as gdc
import sd_material_ui
from flask import current_app
from urllib.parse import parse_qs, urlencode

# Local imports:
import data_controller
from networks.cytoscape_stylesheet.BaseStylesheet import BaseStylesheet
from networks.controls_sidebar_decorator.ControlsSidebar import ControlsSidebar
from networks.controls_sidebar_decorator.factory_sidebar_decorator import factory_sidebar_decorator
from networks.controls_sidebar_decorator.factory_sidebar_decorator import bind_controls_sidebar_callbacks

TIME_DIV = 60 * 60 * 24 * 30

selection_params = {'wikis', 'network', 'lower_bound', 'upper_bound'}

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

    # Contructs the assets_url_path for image sources:
    assets_url_path = os.path.join('/app/', 'assets') #TOCHANGE: use a config var

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
                    gdc.Import(src='/js/main.share_modal.js')
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
                            dcc.RangeSlider(
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
                        'height': '65vh',
                        'width': 'calc(100% - 300px)'
                    },
                    stylesheet = BaseStylesheet().cy_stylesheet
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
            children=[

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
    ############################
    bind_controls_sidebar_callbacks('co_editing_network', app)
    ############################


    @app.callback(
        Output('ready', 'value'),
        [Input('dates-slider', 'value')]
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
        [Input('initial-selection', 'children')]
    )
    def update_slider(selection_json):
         # get network instance from selection
        selection = json.loads(selection_json)
        wiki = selection['wikis'][0]
        origin = data_controller.get_first_entry(wiki)
        end = data_controller.get_last_entry(wiki)

        origin = int(datetime.strptime(str(origin),
            "%Y-%m-%d %H:%M:%S").strftime('%s'))
        end = int(datetime.strptime(str(end),
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

        return  dcc.RangeSlider(
                    id='dates-slider',
                    min=1,
                    max=max_time,
                    step=1,
                    value=[1, int(2 + max_time / 10)],
                    marks=range_slider_marks
                )


    @app.callback(
        Output('download-button', 'href'),
        [Input('dates-slider', 'value')],
        [State('url', 'search'),
        State('initial-selection', 'children')]
    )
    def update_download_url(slider, query_string, selection_json):
        if not slider:
            raise PreventUpdate()

        selection = json.loads(selection_json)
        wiki = selection['wikis'][0]

        # Attention! query_string includes heading ? symbol
        query_string_dict = parse_qs(query_string[1:])

        # get only the parameters we are interested in for the side_bar selection
        selection = { param: query_string_dict[param] for param in set(query_string_dict.keys()) & selection_params }

        # Let's parse the time values
        first_entry = data_controller.get_first_entry(wiki)
        first_entry = int(datetime.strptime(str(first_entry), "%Y-%m-%d %H:%M:%S").strftime('%s'))
        upper_bound = first_entry + slider[1] * TIME_DIV
        lower_bound = first_entry + slider[0] * TIME_DIV

        # Now, time to update the query
        selection['upper_bound'] = upper_bound
        selection['lower_bound'] = lower_bound
        new_query = urlencode(selection,  doseq=True)
        href = f'/download/?{new_query}'

        if debug:
            print(f'Download href updated to: {href}')

        return href
