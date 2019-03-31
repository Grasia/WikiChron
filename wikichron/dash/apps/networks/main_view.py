"""
    main_view.py

    Descp: This file is used to generate the page content

    Created on: 31/03/2019

    Copyright 2019 Youssef 'FRYoussef' El Faqir el Rhazoui
        <f.r.youssef@hotmail.com>
"""

import os
import json
import pandas as pd

from flask import current_app
import dash_html_components as html
import dash_daq as daq
import dash_core_components as dcc
import grasia_dash_components as gdc
import sd_material_ui
import dash_cytoscape
import dash_table

from .utils import get_mode_config
from .networks.CytoscapeStylesheet import CytoscapeStylesheet
from .networks.models import networks_generator as net_factory
from .networks.models.BaseNetwork import BaseNetwork

IMAGE_HEADER = 'url(../../../static/assets/header_background.png)'
RANKING_EMPTY_HEADER = [{'name': 'User', 'id': 'name'}, 
                        {'name': 'Metric', 'id': 'metric'}]
RANKING_EMPTY_DATA = pd.DataFrame(columns=[RANKING_EMPTY_HEADER[0]['id'], 
    RANKING_EMPTY_HEADER[1]['id']])
PAGE_SIZE = 10

global debug
debug = True if os.environ.get('FLASK_ENV') == 'development' else False


def main_header(selection_url, query_string, mode_config, assets_url_path):
    """
    Generates the main header

    Return: An HTML object with the header content
    """
    href_download_button = f'{mode_config["DASH_DOWNLOAD_PATHNAME"]}{query_string}'
    return (html.Div(
            children=[
                html.Img(src='{}/wikichron_networks_logo2.svg'.format(assets_url_path), 
                    className='title-img'),
                html.Div(children=[
                    html.A('< Go back to selection', href=selection_url, style={'font-weight': 'bold'}),
                    html.Div([
                        html.A(
                            html.Img(src='{}/cloud_download.svg'.format(assets_url_path)),
                            href=href_download_button,
                            id='download-button',
                            target='_blank',
                            className='icon',
                            title='Download data'
                        ),
                        html.A(
                            html.Img(src='{}/share.svg'.format(assets_url_path)),
                            id='share-button',
                            className='icon',
                            title='Share current selection'
                        )
                    ], 
                    className='icons-bar')
                ])
        ], className='main-root-header', style={'background-image': IMAGE_HEADER})
    )


def selection_title(selected_wiki, selected_network):
    selection_text = (f'{selected_network} network for: {selected_wiki}')
    return html.P([selection_text])


def share_modal(share_link, download_link):
    """
    Generates a window to share a link.
    Values for the share link and download link will be set at runtime in a
    dash callback.
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
                html.Div(id='date-slider-container',
                    style={'height': '35px'},
                    children=[
                        dcc.RangeSlider(
                            id='dates-slider'
                    )],
                ),

                html.Div(children=[
                    html.Span('Time interval (months):'),
                    html.Div(children=[
                        html.Button("<<", id="bt-back", n_clicks_timestamp='0'),
                        dcc.Input(id="in-step-slider" , type='number', 
                            placeholder='MM', min='1', max='999'),
                        html.Button(">>", id="bt-forward", n_clicks_timestamp='0'),
                    ]),
                ], className='slider-add-on'),
            ],
            style={'margin-top': '15px', 'display': 'grid'}
            )


def build_slider_pane(selected_wiki_name, selected_network_name):
    header = html.Div(children=[
        selection_title(selected_wiki_name, selected_network_name)
        ], className='header-pane main-header-pane')
    body = html.Div(children=[
        date_slider_control()
    ], className='body-pane')

    return html.Div(children=[header, body], className='pane main-pane')


def cytoscape_component():
    no_data = html.Div(children=[html.P()], 
        id='no-data', className='non-show')
    cytoscape = dash_cytoscape.Cytoscape(
                id='cytoscape',
                className='show',
                elements = [],
                maxZoom = 1.75,
                minZoom = 0.35,
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
                stylesheet = CytoscapeStylesheet.make_basic_stylesheet()
    )
    return html.Div(children=[cytoscape, no_data], className='cyto-dim')


def build_distribution_pane() -> html.Div:
    header = html.Div(children=[
        html.P('Degree Distribution'),
        html.Hr(className='pane-hr'),
        ], className='header-pane sidebar-header-pane')

    left_body = html.Div(children=[
                    html.P('Scale:'),
                    dcc.RadioItems(
                        id='scale',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear'
                    )
                ])
    left = html.Div([header, left_body])

    body = dcc.Graph(id='distribution-graph')

    return html.Div(children=[left, body], className='pane distribution-pane')


def dropdown_color_metric_selector(network_code):
    dict_metrics = net_factory.get_secondary_metrics(network_code)
    options = []
    for k in dict_metrics.keys():
        options.append({
            'label': k,
            'value': k
        })

    return dcc.Dropdown(
        id='dd-color-metric',
        options=options,
        placeholder='Select a metric to color'
    )


def build_network_controls(network_code):
    togg1 = html.Div([
        daq.BooleanSwitch(id='tg-show-labels', className='toggle', on=False),
        html.P('Show labels')
    ])
    togg2 = html.Div([
        daq.BooleanSwitch(id='tg-show-clusters', className='toggle', on=False),
        html.P('Show clusters')
    ])
    left = html.Div([togg1, togg2])
    center = html.Div([
        html.P('Reset View:'),
        html.Button('Reset', id='reset_cyto')
    ])
    right = dropdown_color_metric_selector(network_code)
    return html.Div(children=[left, center, right])


def build_network_stats(stats: list()) -> html.Div:
    header = html.Div(children=[
        'Network Stats',
        html.Hr(className='pane-hr')
        ], className='header-pane sidebar-header-pane')

    body = html.Div(children=[
            html.Div([
                html.P(f'{stats[0]}: ...'),
                html.P(f'{stats[1]}: ...')
            ]),
            html.Div([
                html.P(f'{stats[2]}: ...'),
                html.P(f'{stats[3]}: ...')
            ])], id='net-stats', className='body-pane')

    return html.Div(children=[header, body], className='pane side-pane')


def build_table(network_code) -> html.Div:
    dict_metrics = net_factory.get_available_metrics(network_code)
    options = []
    for k in dict_metrics.keys():
        options.append({
            'label': k,
            'value': k
        })

    header = html.Div(children=[
        'Ranking',
        html.Hr(className='pane-hr')
    ],
    className='header-pane sidebar-header-pane')

    body = html.Div(children=[
            html.Div([dcc.Dropdown(
                id='dd-local-metric',
                options=options,
                placeholder='Select a local metric'
            )]),
            dash_table.DataTable(
                id='ranking-table',
                pagination_settings={
                    'current_page': 0,
                    'page_size': PAGE_SIZE
                },
                pagination_mode='be',
                sorting='be',
                sorting_type='single',
                sorting_settings=[],
                row_selectable="multi",
                selected_rows=[],
                style_as_list_view=True,
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': '600'
                },
                data = RANKING_EMPTY_DATA.to_dict('rows'),
                columns = RANKING_EMPTY_HEADER,
            )], 
            className='body-pane')

    return html.Div(children=[header, body], className='pane side-pane')


def build_user_stats() -> html.Div:
    header = html.Div(children=[
        'User Stats',
        html.Hr(className='pane-hr')
    ], 
    className='header-pane sidebar-header-pane')

    body = html.Div(id='user-stats', children=['Please, click on a node to show it\'s info'], 
        className='body-pane')
    return html.Div(children=[header, body], className='pane side-pane')


def build_sidebar(network_code) -> html.Div:
    """
    Use this function in order to build and get the side elements
    """
    return html.Div(className='', children=[
        build_network_stats(list(BaseNetwork.get_network_stats().keys())),
        build_table(network_code),
        build_user_stats()
    ])


def build_foot(assets_url_path):
    return html.Div(children=[
        html.P('Developded by Youssef El Faqir El Rhazoui'),
        html.Div([
            html.A(
                html.Img(src='{}/ico-github.svg'.format(assets_url_path)),
                href='https://github.com/Grasia/WikiChron-networks',
                target='_blank',
                className='icon',
                title='Github repo'
            ),
            html.P('GitHub'),
            html.A(
                html.Img(src='{}/documentation.svg'.format(assets_url_path)),
                href='https://github.com/Grasia/WikiChron/wiki/',
                target='_blank',
                className='icon',
                title='Documentation'
            ),
            html.P('Docs'),
        ])
    ], className='foot')


def generate_main_content(wikis_arg, network_type_arg, query_string):
    """
    It generates the main content
    Parameters:
        -wikis_arg: wikis to show, only used the first wiki
        -network_type_arg: type of network to generate
        -query_string: string for the download button

    Return: An HTML object with the main content
    """

    # Load app config
    server_config = current_app.config
    mode_config = get_mode_config(current_app)

    # Contructs the assets_url_path for image sources:
    assets_url_path = os.path.join(mode_config['DASH_BASE_PATHNAME'], 'assets')

    if debug:
        print ('Generating main...')

    network_type_code = network_type_arg['code']
    args_selection = json.dumps({"wikis": wikis_arg, "network": network_type_code})

    selected_wiki_name = wikis_arg[0]['name']
    selected_network_name = network_type_arg['name']

    share_url_path = f'{server_config["PREFERRED_URL_SCHEME"]}://{server_config["APP_HOSTNAME"]}{mode_config["DASH_BASE_PATHNAME"]}{query_string}'
    download_url_path = f'{server_config["PREFERRED_URL_SCHEME"]}://{server_config["APP_HOSTNAME"]}{mode_config["DASH_DOWNLOAD_PATHNAME"]}{query_string}'
    selection_url = f'{mode_config["HOME_MODE_PATHNAME"]}'

    main = html.Div(
            id='main',
            className='control-text',
            children=[
                build_slider_pane(selected_wiki_name, selected_network_name),
                share_modal(share_url_path, download_url_path),
                html.Div(id='initial-selection', style={'display': 'none'},
                            children=args_selection),
                build_network_controls(network_type_code),
                html.Div([
                    cytoscape_component(),
                    build_distribution_pane()
                ]),

                # Signal data
                html.Div(id='network-ready', style={'display': 'none'}),
                html.Div(id='signal-data', style={'display': 'none'}),
                html.Div(id='ready', style={'display': 'none'}),
                html.Div(id='highlight-node', style={'display': 'none'})
            ])

    header = main_header(selection_url, query_string, mode_config, assets_url_path)

    body = html.Div(children = [
        main,
        build_sidebar(network_type_code)
    ], className='body')

    foot = build_foot(assets_url_path)

    return html.Div(children = [header, body, foot])