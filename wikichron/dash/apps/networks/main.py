#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   main.py

   Descp: This script generates the main content of the site, this content includes
serveral interpretations of the network, which is generated from the wikis
data.

   Created on: 07-dec-2018

   Copyright 2018-2019 Youssef 'FRYoussef' El Faqir El Rhazoui <f.r.youssef@hotmail.com>
"""

# Built-in imports
import os
import time
import json
from datetime import datetime
import dash
import dash_cytoscape
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_table
import plotly.graph_objs as go
import grasia_dash_components as gdc
import sd_material_ui
from flask import current_app
from urllib.parse import parse_qs, urlencode

# Local imports:
from . import data_controller
from .utils import get_mode_config
from .networks.models import networks_generator as net_factory
from .networks.CytoscapeStylesheet import CytoscapeStylesheet
from .right_side_bar import build_sidebar, bind_sidebar_callbacks

TIME_DIV = 60 * 60 * 24 * 30
IMAGE_HEADER = 'url(../../../static/assets/header_background.png)'
selection_params = {'wikis', 'network', 'lower_bound', 'upper_bound'}

global debug
debug = True if os.environ.get('FLASK_ENV') == 'development' else False


def update_query_by_time(wiki, query_string, up_val, low_val):
    query_string_dict = parse_qs(query_string)

    # get only the parameters we are interested in for the side_bar selection
    selection = { param: query_string_dict[param] for param in set(query_string_dict.keys()) & selection_params }

    # Let's parse the time values
    first_entry = data_controller.get_first_entry(wiki)
    first_entry = int(datetime.strptime(str(first_entry), "%Y-%m-%d %H:%M:%S").strftime('%s'))
    upper_bound = first_entry + up_val * TIME_DIV
    lower_bound = first_entry + low_val * TIME_DIV

    # Now, time to update the query
    selection['upper_bound'] = upper_bound
    selection['lower_bound'] = lower_bound
    return urlencode(selection,  doseq=True)


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


    def main_header(selection_url):
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
                        html.Span(id='slider-desc',
                        children=[
                            html.Strong('Time interval (months):')
                        ]),

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
        no_data = html.Div(children=[html.P('Nothing to show')], 
            id='no-data', className='non-show cyto-dim')
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
                    style = {
                        'height': '65vh',
                        'width': '100%'
                    },
                    stylesheet = CytoscapeStylesheet.make_basic_stylesheet()
        )
        return html.Div(style={'display': 'flex'}, children=[cytoscape, no_data])


    def build_distribution_pane() -> html.Div:
        header = html.Div(children=[
            html.P('Degree Distribution')
            ], className='header-pane main-header-pane')
        return html.Div([
            dcc.RadioItems(
                id='scale',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            ),
            dcc.Graph(
                id='distribution-graph'
            )
        ])


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
            daq.BooleanSwitch(id='tg-show-labels', on=False),
            html.P('Show labels')
        ])
        togg2 = html.Div([
            daq.BooleanSwitch(id='tg-show-clusters', on=False),
            html.P('Show clusters')
        ])
        left = html.Div([togg1, togg2])
        right = dropdown_color_metric_selector(network_code)
        return html.Div(children=[left, right])


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
                cytoscape_component(),
                build_distribution_pane(),

                # Signal data
                html.Div(id='network-ready', style={'display': 'none'}),
                html.Div(id='signal-data', style={'display': 'none'}),
                html.Div(id='ready', style={'display': 'none'}),
                html.Div(id='metric-to-show', style={'display': 'none'}),
                html.Div(id='highlight-node', style={'display': 'none'})
            ])

    header = main_header(selection_url)

    body = html.Div(children = [
        main,
        build_sidebar()
    ], className='body')

    return html.Div(children = [header, body])


def bind_callbacks(app):

    # Right sidebar callbacks
    bind_sidebar_callbacks(app)


    @app.callback(
        Output('highlight-node', 'value'),
        [Input('ranking-table', 'derived_virtual_data'),
        Input('ranking-table', 'derived_virtual_selected_rows')]
    )
    def highlight_node(data, selected):
        if not data:
            raise PreventUpdate()

        # Reset the stylesheet
        if not selected:
            return None

        # highlight nodes selected
        selection = [data[s] for s in selected]
        return selection


    @app.callback(
        Output('network-ready', 'value'),
        [Input('ready', 'value')],
        [State('initial-selection', 'children'),
        State('dates-slider', 'value')]
    )
    def update_network(ready, selection_json, slider):
        if not ready or not slider:
            raise PreventUpdate()

        # get network instance from selection
        selection = json.loads(selection_json)
        wiki = selection['wikis'][0]
        network_code = selection['network']

        if debug:
            print(f'Updating network with values:\
            \n\t- wiki: {wiki["url"]}\
            \n\t- network: {network_code}\
            \n\t- slider: ({slider[0]},{slider[1]})')

        print(' * [Info] Building the network....')
        time_start_calculations = time.perf_counter()
        (lower_bound, upper_bound) = data_controller\
                .get_time_bounds(wiki, slider[0], slider[1])
        network = data_controller.get_network(wiki, network_code, lower_bound, upper_bound)

        time_end_calculations = time.perf_counter() - time_start_calculations
        print(f' * [Timing] Network ready in {time_end_calculations} seconds')

        return network.to_cytoscape_dict()


    @app.callback(
        Output('cytoscape', 'stylesheet'),
        [Input('cytoscape', 'elements'),
        Input('tg-show-labels', 'on'),
        Input('tg-show-clusters', 'on'),
        Input('highlight-node', 'value'),
        Input('dd-color-metric', 'value')],
        [State('network-ready', 'value'),
        State('initial-selection', 'children')]
    )
    def update_stylesheet(_, lb_switch, clus_switch, nodes_selc, dd_val,
        cy_network, selection_json):

        if not cy_network:
            raise PreventUpdate()

        selection = json.loads(selection_json)
        network_code = selection['network']

        directed = net_factory.is_directed(network_code)
        stylesheet = CytoscapeStylesheet(directed=directed)
        metric = {}

        if dd_val:
            metric = net_factory.get_secondary_metrics(network_code)[dd_val]

        if not nodes_selc:
            stylesheet.all_transformations(cy_network, metric)
        else:
            stylesheet.highlight_nodes(cy_network, nodes_selc)

        if lb_switch:
            stylesheet.set_label('label')
        else:
            stylesheet.set_label('')

        if clus_switch:
            stylesheet.color_nodes_by_cluster()
        else:
            stylesheet.color_nodes(cy_network, metric)

        return stylesheet.cy_stylesheet


    ####################################
    # TODO Remove this function is useless
    ####################################
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
        if not cy_network and 'network' not in cy_network:
            raise PreventUpdate()

        return cy_network['network']


    @app.callback(
        [Output('cytoscape', 'className'),
        Output('no-data', 'className'),
        Output('no-data', 'children')],
        [Input('cytoscape', 'elements')],
        [State('initial-selection', 'children'),
        State('dates-slider', 'value')]
    )
    def check_available_data(cyto, selection_json, slider):
        """
        Checks if there's a network to plot
        """
        if not slider:
            raise PreventUpdate()

        cyto_class = 'show'
        no_data_class = 'non-show cyto-dim'
        no_data_children = []
        if not cyto:
            cyto_class = 'non-show'
            no_data_class = 'show cyto-dim'

            selection = json.loads(selection_json)
            wiki = selection['wikis'][0]
            first_entry = data_controller.get_first_entry(wiki)
            first_entry = int(datetime.strptime(str(first_entry), "%Y-%m-%d %H:%M:%S").strftime('%s'))
            upper_bound = first_entry + slider[1] * TIME_DIV
            lower_bound = first_entry + slider[0] * TIME_DIV
            upper_bound = datetime.fromtimestamp(upper_bound).strftime('%B/%Y')
            lower_bound = datetime.fromtimestamp(lower_bound).strftime('%B/%Y')

            no_data_children = [
                html.P('Nothing to show,'),
                html.P(f'no data available between {lower_bound} and {upper_bound}.'),
                html.P('Please, try changing the date selection.')
            ]

        return cyto_class, no_data_class, no_data_children


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
        [Input('initial-selection', 'children')],
        [State('url', 'search')]
    )
    def update_slider(selection_json, query_string):
         # get network instance from selection
        selection = json.loads(selection_json)
        wiki = selection['wikis'][0]

        # Attention! query_string includes heading ? symbol
        query_string_dict = parse_qs(query_string[1:])

        # get only the parameters we are interested in for the side_bar selection
        selection = { param: query_string_dict[param] for param in set(query_string_dict.keys()) & selection_params }

        origin = data_controller.get_first_entry(wiki)
        end = data_controller.get_last_entry(wiki)

        origin = int(datetime.strptime(str(origin),
            "%Y-%m-%d %H:%M:%S").strftime('%s'))
        end = int(datetime.strptime(str(end),
            "%Y-%m-%d %H:%M:%S").strftime('%s'))

        time_gap = end - origin
        max_time = time_gap // TIME_DIV

        if all(k in selection for k in ('lower_bound', 'upper_bound')):
            low_val = (int(selection['lower_bound'][0]) - origin) // TIME_DIV
            upper_val = (int(selection['upper_bound'][0]) - origin) // TIME_DIV
        else:
            low_val = 1
            upper_val = int(2 + max_time / 10)

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
                    value=[low_val, upper_val],
                    marks=range_slider_marks
                )


    @app.callback(
        Output('dates-slider', 'value'),
        [Input('bt-back', 'n_clicks_timestamp'),
        Input('bt-forward', 'n_clicks_timestamp')],
        [State('in-step-slider', 'value'),
        State('date-slider-container', 'children')]
    )
    def move_slider_range(bt_back, bt_forward, step, di_slider):
        """
        Controls to move the slider selection
        """
        if not step:
            raise PreventUpdate()

        step = int(step)

        if bt_back and int(bt_back) > int(bt_forward):
            step = -step
        elif not (bt_forward and int(bt_forward) > int(bt_back)):
            raise PreventUpdate()

        # step value is in [0, n] | n € N
        # if bt_forward is pressed, the step value will be a positive value

        old_upper = di_slider['props']['value'][0]
        old_lower = di_slider['props']['value'][1]
        upper = di_slider['props']['value'][0]
        lower = di_slider['props']['value'][1]
        max_val = di_slider['props']['max']
        min_val = di_slider['props']['min']

        if upper + step > max_val:
            upper = max_val
        elif upper + step < min_val:
            upper = min_val
        else:
            upper = upper + step

        if lower + step < min_val:
            lower = min_val
        elif lower + step > max_val:
            lower = max_val
        else:
            lower = lower + step
        # Let's check if the input will change the slider
        if lower == old_lower and upper == old_upper:
             raise PreventUpdate('Slider will not change')

        return [upper, lower]


    @app.callback(
        Output('download-button', 'href'),
        [Input('dates-slider', 'value')],
        [State('download-button', 'href'),
        State('initial-selection', 'children')]
    )
    def update_download_url(slider, query_string, selection_json):
        if not slider:
            raise PreventUpdate()
        selection = json.loads(selection_json)
        wiki = selection['wikis'][0]

        query_splited = query_string.split("?")
        new_query = update_query_by_time(wiki, query_splited[1], slider[1], slider[0])
        href = f'{query_splited[0]}?{new_query}'

        if debug:
            print(f'Download href updated to: {href}')

        return href


    @app.callback(
        Output('share-link-input', 'value'),
        [Input('dates-slider', 'value')],
        [State('share-link-input', 'value'),
        State('initial-selection', 'children')]
    )
    def update_share_url(slider, query_string, selection_json):
        if not slider:
            raise PreventUpdate()
        selection = json.loads(selection_json)
        wiki = selection['wikis'][0]

        query_splited = query_string.split("?")
        new_query = update_query_by_time(wiki, query_splited[1], slider[1], slider[0])
        new_query = f'{query_splited[0]}?{new_query}'
        if debug:
            print(f'Share link updated to: {new_query}')

        return new_query


    @app.callback(
        Output('distribution-graph', 'figure'),
        [Input('scale', 'value'),
        Input('dates-slider', 'value')],
        [State('initial-selection', 'children')]
    )
    def update_graph(scale_type, slider, selection_json):
        if not slider:
            raise PreventUpdate()

        selection = json.loads(selection_json)
        wiki = selection['wikis'][0]
        network_code = selection['network']
        (lower, upper) = data_controller.get_time_bounds(wiki, slider[0], slider[1])
        network = data_controller.get_network(wiki, network_code, lower, upper)

        (k, p_k) = network.get_degree_distribution()

        return {
            'data': [go.Scatter(
                x=k,
                y=p_k,
                mode='markers',
                marker={
                    'size': 15,
                    'opacity': 0.5,
                    'line': {'width': 0.5, 'color': 'white'}
                }
            )],
            'layout': go.Layout(
                title='Degree Distribution',
                xaxis={
                    'title': 'K',
                    'type': 'linear' if scale_type == 'Linear' else 'log'
                },
                yaxis={
                    'title': 'P_k',
                    'type': 'linear' if scale_type == 'Linear' else 'log'
                },
                margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
                height=450,
                hovermode='closest'
            )
        }
