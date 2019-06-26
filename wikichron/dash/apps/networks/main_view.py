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
from . import data_controller

RANKING_EMPTY_HEADER = [{'name': 'Editor', 'id': 'name'},
                        {'name': 'Metric', 'id': 'metric'}]
RANKING_EMPTY_DATA = pd.DataFrame(columns=[RANKING_EMPTY_HEADER[0]['id'],
    RANKING_EMPTY_HEADER[1]['id']])
PAGE_SIZE = 10
NO_DATA_NODE_STATS_HEADER = 'Editor Stats'
NO_DATA_NODE_STATS_BODY = 'Please, click on a node to show its info'

DEFAULT_LEGEND_TEXT = {}
DEFAULT_LEGEND_TEXT['min_node_color'] = 'Select a metric to color'
DEFAULT_LEGEND_TEXT['max_node_color'] = 'Select a metric to color'
DEFAULT_LEGEND_TEXT['min_node_size'] = 'Select a metric to size'
DEFAULT_LEGEND_TEXT['max_node_size'] = 'Select a metric to size'
DEFAULT_LEGEND_TEXT['min_edge_size'] = 'A weak interaction in the wiki'
DEFAULT_LEGEND_TEXT['max_edge_size'] = 'A strong interaction in the wiki'

global debug
debug = True if os.environ.get('FLASK_ENV') == 'development' else False


def main_header(selection_url, query_string, mode_config, assets_url_path):
    """
    Generates the main header

    Return: An HTML object with the header content
    """
    href_download_button = f'{mode_config["DASH_DOWNLOAD_PATHNAME"]}{query_string}'
    return (html.Div(
            id='header',
            children=[
                html.Div(
                    id='header-container',
                    children=[
                        html.Img(src='{}/wikichron_networks_logo2.svg'.format(assets_url_path),
                            id='title-img'),
                        html.Hr(),
                        html.Div(children=[
                            html.Div([
                                html.A('< Go back to selection', href=selection_url),
                                html.A('Switch network >', id='switch-network')
                            ]),
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
                                    href='https://github.com/Grasia/WikiChron',
                                    target='_blank',
                                    className='icon',
                                    title='Github repo'
                                )
                            ],
                            className='icons-bar')
                        ], className='root-header-elems')
                    ]
                )
            ], className='main-root-header'
        )
    )


def selection_title(selected_wiki, selected_network):
    selection_text = (f'{selected_network} network for: {selected_wiki}')
    return html.P([selection_text])


def inflate_switch_network_dialog(link, network_code):
    nets = net_factory.create_available_networks()
    codes = [n.CODE for n in nets]
    names = [n.NAME for n in nets]
    opts = [{'label': l, 'value': v} for l, v in zip(names, codes)]

    return html.Div([
                html.H4('Please, select a network to switch'),
                dcc.RadioItems(
                    id='radio-network-type',
                    options=opts,
                    value=network_code
                ),
                html.Div(children=[
                    html.A('Open in this tab', id='this-switch-network', href=link),
                    html.A('Open in a new tab', id='new-switch-network', target='_blank', href=link)
                ])
            ], className='dialog-content')


def inflate_share_dialog(share_link):
    return html.Div(children=[
                html.H4('Share WikiChron with others!'),
                html.P([
                    html.Strong('Link with your current selection:'),
                    html.Div(className='share-modal-link-and-button-cn', children=[
                    dcc.Input(value=share_link, id='share-link-input', readOnly=True, className='share-modal-input-cn', type='url'),
                    html.Div(className='tooltip', children=[
                        html.Button('Copy!', id='share-link', className='share-modal-button-cn'),
                    ])
                    ]),
                ]),
                gdc.Import(src='/js/common/dash/main.share_modal.js')
                ],
                className='dialog-content')


def build_dilog():
    return html.Div([
        sd_material_ui.Dialog(
            children=[],
            id='dialog',
            modal=False,
            open=False
        )
    ])


def date_slider_control(assets_url_path):
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
                    html.Span('Slide the time window:'),
                    html.Div(children=[
                        html.A(
                            html.Img(src=f"{assets_url_path}/arrow-left.svg", className="arrow"),
                            id="bt-back"
                        ),
                        dcc.Input(id="in-step-slider" , type='number',
                            placeholder='MM', min='1', max='999'),
                        html.A(
                            html.Img(src=f"{assets_url_path}/arrow-right.svg", className="arrow"),
                            id="bt-forward"
                        ),
                    ], className='slider-controls-pane'),
                ], className='slider-add-on'),
            ],
            style={'margin-top': '15px', 'display': 'grid'}
            )


def build_slider_pane(selected_wiki_name, selected_network_name, assets_url_path):
    header = html.Div(children=[
        selection_title(selected_wiki_name, selected_network_name)
        ], className='header-pane main-header-pane')
    body = html.Div(children=[
        date_slider_control(assets_url_path)
    ], className='body-pane')

    return html.Div(children=[header, body], className='pane main-pane')


def build_network_controls(network_code):
    togg1 = html.Div(children=[
        daq.BooleanSwitch(id='tg-show-labels', className='toggle', on=True),
        html.P('Show labels')
    ], className='net-control')

    togg2 = html.Div(children=[
        daq.BooleanSwitch(id='tg-show-clusters', className='toggle', on=False),
        html.P('Show clusters')
    ], className='net-control')

    togg3 = html.Div(children=[
        daq.BooleanSwitch(id='tg-hide-legend', className='toggle', on=True),
        html.P('Show legend')
    ], className='net-control')

    left = html.Div(children=[togg3, togg1, togg2], className='toggle-container')

    center = html.Div(children=[
        html.P('Reset View:'),
        html.Button('Reset', id='reset_cyto')
    ], className='net-control')

    # metrics to fill dropdowns
    dict_metrics = net_factory.get_metrics_to_plot(network_code)
    options = []
    for k in dict_metrics.keys():
        options.append({
            'label': k,
            'value': k
        })

    right = html.Div(children=[
        html.Div(children=[
            'Color:',
            dcc.Dropdown(
                id='dd-color-metric',
                options=options,
                placeholder='Select a metric',
                className='metric-selector'
            )
        ], className='controls-right controls-right-spacer'),

        html.Div(children=[
            'Size:',
            dcc.Dropdown(
                id='dd-size-metric',
                options=options,
                placeholder='Select a metric',
                className='metric-selector',
                value=options[0]['value']
            )
        ], className='controls-right'),
    ], className='controls-right')

    return html.Div(children=[left, center, right], className='controls-container')


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


def build_legend(network_code: str) -> html.Div:
    return html.Div([
        html.Div(children=[
            html.Div(children=[], className='legend-node',
                style={'background-color': CytoscapeStylesheet.N_MIN_COLOR}),
            html.Div(children=[], className='legend-node',
                style={'background-color': CytoscapeStylesheet.N_DEFAULT_COLOR}),
            html.Div(children=[], className='legend-edge',
                style={'background-color': CytoscapeStylesheet.E_DEFAULT_COLOR}),
        ], className='legend-col col1-legend'),

        html.Div(children=[
            html.P(DEFAULT_LEGEND_TEXT['min_node_color'], id='legend-min-node-color'),
            html.P(DEFAULT_LEGEND_TEXT['min_node_size'], id='legend-min-node-size'),
            html.P(DEFAULT_LEGEND_TEXT['min_edge_size'], id='legend-min-edge-edge')
        ], className='legend-col col2-legend'),

        html.Div(children=[
            html.Div(children=[], className='legend-node',
                style={'background-color': CytoscapeStylesheet.N_MAX_COLOR}),
            html.Div(children=[], className='legend-node node-sized',
                style={'background-color': CytoscapeStylesheet.N_DEFAULT_COLOR}),
            html.Div(children=[], className='legend-edge edge-sized',
                style={'background-color': CytoscapeStylesheet.E_DEFAULT_COLOR}),
        ], className='legend-col col3-legend'),

        html.Div(children=[
            html.P(DEFAULT_LEGEND_TEXT['max_node_color'], id='legend-max-node-color'),
            html.P(DEFAULT_LEGEND_TEXT['max_node_size'], id='legend-max-node-size'),
            html.P(DEFAULT_LEGEND_TEXT['max_edge_size'], id='legend-max-edge-size')
        ], className='legend-col col4-legend'),

    ], id='legend', className='pane')


def build_distribution_pane() -> html.Div:
    header = html.Div(children=[
        html.P('Degree Distribution'),
        html.Hr(className='pane-hr'),
        ], className='header-pane sidebar-header-pane')

    left_body = html.Div(children=[
                    html.P('Scale:'),
                    dcc.RadioItems(
                        id='scale',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log', 'Log-Log']],
                        value='Linear'
                    )
                ], className='left-distribution-body')

    left = html.Div(children=[header, left_body], className='left-distribution-pane')

    body = dcc.Graph(id='distribution-graph')

    return html.Div(children=[left, body], className='pane distribution-pane')


def build_network_stats(network_code: str) -> html.Div:
    header = html.Div(children=[
        'Network Stats',
        html.Hr(className='pane-hr')
        ], className='header-pane sidebar-header-pane')

    # construct body
    stats = net_factory.get_network_stats(network_code)
    child = []
    i = 0
    group = []
    for k, _ in stats.items():
        group.append(html.Div(children=[
            html.P(f'{k}:'),
            html.P('...')
        ]))

        i += 1
        if i % 2 == 0:
            child.append(html.Div(children=group))
            group = []
    if group:
        child.append(html.Div(children=group))

    body = html.Div(children=child, id='net-stats', className='body-pane')
    return html.Div(children=[header, body], className='pane side-pane')


def build_ranking(network_code) -> html.Div:
    dict_metrics = net_factory.get_metrics_to_show(network_code)
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
            html.Div(children=[dcc.Dropdown(
                id='dd-local-metric',
                value=options[0]['label'],
                options=options,
                placeholder='Select a local metric'
            )], className='ranking-selection'),
            dash_table.DataTable(
                id='ranking-table',
                columns = RANKING_EMPTY_HEADER,
                data = RANKING_EMPTY_DATA.to_dict('rows'),
                filtering=True,
                sorting=True,
                sorting_type='single',
                sorting_settings=[],
                row_selectable="multi",
                selected_rows=[],
                style_as_list_view=True,
                pagination_mode='fe',
                pagination_settings={
                    "displayed_pages": 1,
                    'current_page': 0,
                    'page_size': PAGE_SIZE
                },
                navigation="page",
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': '600'
                },
            )],
            className='body-pane')

    return html.Div(children=[header, body], className='pane side-pane')


def build_node_stats() -> html.Div:
    header = html.Div(children=[
        html.Span(NO_DATA_NODE_STATS_HEADER, id='user-stats-title'),
        html.Hr(className='pane-hr')
    ],
    className='header-pane sidebar-header-pane')

    body = html.Div(id='user-stats', children=[NO_DATA_NODE_STATS_BODY],
        className='body-pane')
    return html.Div(children=[header, body], className='pane side-pane')


def build_sidebar(network_code) -> html.Div:
    """
    Use this function in order to build and get the side elements
    """
    return html.Div(className='sidebar', children=[
        build_network_stats(network_code),
        build_ranking(network_code),
        build_node_stats()
    ])


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
    mode_config = get_mode_config(current_app)

    # Contructs the assets_url_path for image sources:
    assets_url_path = os.path.join(mode_config['DASH_STATIC_PATHNAME'], 'assets')

    if debug:
        print ('Generating main...')

    network_type_code = network_type_arg['code']
    args_selection = json.dumps({"wikis": wikis_arg, "network": network_type_code})

    selected_wiki = wikis_arg[0]
    selected_wiki_name = selected_wiki['name']
    selected_network_name = network_type_arg['name']
    selection_url = f'{mode_config["HOME_MODE_PATHNAME"]}selection/{query_string}'

    (time_index_beginning, time_index_end) = data_controller.calculate_indices_all_months(selected_wiki)

    time_index_beginning = json.dumps(time_index_beginning.date.tolist(), default=str)
    time_index_end = json.dumps(time_index_end.date.tolist(), default=str)

    main = html.Div(
            id='main',
            className='control-text',
            children=[
                build_slider_pane(selected_wiki_name, selected_network_name, assets_url_path),
                build_dilog(),
                html.Div(id='initial-selection', style={'display': 'none'},
                            children=args_selection),
                build_network_controls(network_type_code),
                html.Div([
                    html.Div([
                        build_legend(network_type_code),
                        cytoscape_component()
                    ]),
                    build_distribution_pane()
                ], className='left-body'),

                # Signal data
                html.Div(id='network-ready', style={'display': 'none'}),
                html.Div(id='old-state-node', style={'display': 'none'}),
                html.Div(id='highlight-node', style={'display': 'none'}),
                html.Div(id='dates-index', className='time-index', children=time_index_beginning, style={'display': 'none'}),
                html.Div(id='dates-index-end', children=time_index_end, style={'display': 'none'})
            ])

    header = main_header(selection_url, query_string, mode_config, assets_url_path)

    body = html.Div(children=[
        main,
        build_sidebar(network_type_code)
    ], className='body')

    labels_script = gdc.Import(src='/js/common/dash/sliderHandlerLabels.js')
    filter_script = gdc.Import(src='/js/networks/dash/filterInfo.js')
    return html.Div(children = [header, body, labels_script, filter_script])
