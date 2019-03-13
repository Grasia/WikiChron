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
from dash.exceptions import PreventUpdate
import dash_table
import plotly.graph_objs as go
import grasia_dash_components as gdc
import sd_material_ui
from flask import current_app
from urllib.parse import parse_qs, urlencode

# Local imports:
import data_controller
import networks.models.networks_generator as net_factory
from networks.cytoscape_stylesheet.BaseStylesheet import BaseStylesheet
from networks.controls_sidebar_decorator.ControlsSidebar import ControlsSidebar
from networks.controls_sidebar_decorator.factory_sidebar_decorator import factory_sidebar_decorator
from networks.controls_sidebar_decorator.factory_sidebar_decorator import bind_controls_sidebar_callbacks

TIME_DIV = 60 * 60 * 24 * 30

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
        -network_type_arg, type of network to generate
        -query_string: string to share/download
        -APP_HOSTNAME: url to share/download

    Return: An HTML object with the main content
    """

    # Load app config
    config = current_app.config
    # Contructs the assets_url_path for image sources:
    assets_url_path = os.path.join(config['DASH_BASE_PATHNAME'], 'assets')


    def main_header():
        """
        Generates the main header

        Return: An HTML object with the header content
        """
        href_download_button = f'{config["DASH_DOWNLOAD_PATHNAME"]}{query_string}'
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

                    html.Div(children=[
                        html.Span(id='slider-header',
                        children=[
                            html.Strong(
                                'Time interval (months):'),
                            html.Span(id='display-slider-selection')
                        ]),

                        html.Div(children=[
                            html.Button("<<", id="bt-back", n_clicks_timestamp='0', className='step-button'),
                            dcc.Input(id="in-step-slider" , type='number', value='1', min='0'),
                            html.Button(">>", id="bt-forward", n_clicks_timestamp='0', className='step-button'),
                        ], className='slider-controls'),
                    ],
                    style={'display': 'flex'}),

                    html.Div(id='date-slider-container',
                        style={'height': '35px'},
                        children=[
                            dcc.RangeSlider(
                                id='dates-slider'
                        )],
                    )
                ],
                style={'margin-top': '15px', 'display': 'grid'}
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


    def ranking_table():
        return dash_table.DataTable(
                    id='ranking-table',
                    pagination_settings={
                        'current_page': 0,
                        'page_size': 10
                    },
                    pagination_mode='be',
                    sorting='be',
                    sorting_type='single',
                    sorting_settings=[],
                    style_cell={'textAlign': 'center'},
                    style_header={'fontWeight': 'bold'},
                    row_selectable="multi",
                    selected_rows=[],
                )


    def distribution_graph():
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


    if debug:
        print ('Generating main...')

    network_type_code = network_type_arg['code']
    args_selection = json.dumps({"wikis": wikis_arg, "network": network_type_code})

    selected_wiki_name = wikis_arg[0]['name']
    selected_network_name = network_type_arg['name']

    controls_sidebar = ControlsSidebar()
    sidebar_decorator = factory_sidebar_decorator(network_type_code, controls_sidebar)
    sidebar_decorator.add_all_sections()

    share_url_path = f'{config["APP_HOSTNAME"]}{config["DASH_BASE_PATHNAME"]}{query_string}'
    download_url_path = f'{config["APP_HOSTNAME"]}{config["DASH_DOWNLOAD_PATHNAME"]}{query_string}'

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

                share_modal(share_url_path, download_url_path),

                html.Div(id='initial-selection', style={'display': 'none'},
                            children=args_selection),

                cytoscape_component(),
                ranking_table(),
                distribution_graph(),
                html.Div(id='user-info'),

                html.Div(id='network-ready', style={'display': 'none'}),
                html.Div(id='signal-data', style={'display': 'none'}),
                html.Div(id='ready', style={'display': 'none'}),
                html.Div(id='metric-to-show', style={'display': 'none'}),
                html.Div(id='highlight-node', style={'display': 'none'})
        ])


def bind_callbacks(app):

    # Right sidebar callbacks
    ############################
    bind_controls_sidebar_callbacks('co_editing_network', app)
    ############################


    @app.callback(
        Output('ranking-table', 'columns'),
        [Input('metric-to-show', 'value')],
        [State('network-ready', 'value'),
        State('initial-selection', 'children'),
        State('dates-slider', 'value')]
    )
    def update_ranking_header(metric, ready, selection_json, slider):
        if not ready or not metric or not slider:
            print('not ready header')
            raise PreventUpdate()

        selection = json.loads(selection_json)
        wiki = selection['wikis'][0]
        network_code = selection['network']
        (lower, upper) = data_controller.get_time_bounds(wiki, slider[0], slider[1])
        network = data_controller.get_network(wiki, network_code, lower, upper)

        df = network.get_metric_dataframe(metric)
        return [{"name": i, "id": i} for i in df.columns]


    @app.callback(
        Output('ranking-table', 'data'),
        [Input('ranking-table', 'pagination_settings'),
        Input('ranking-table', 'sorting_settings'),
        Input('metric-to-show', 'value'),
        Input('dates-slider', 'value')],
        [State('network-ready', 'value'),
        State('initial-selection', 'children')]
    )
    def update_ranking(pag_set, sort_set, metric, slider, ready, selection_json):
        if not ready or not metric or not slider:
            raise PreventUpdate()

        selection = json.loads(selection_json)
        wiki = selection['wikis'][0]
        network_code = selection['network']
        (lower, upper) = data_controller.get_time_bounds(wiki, slider[0], slider[1])
        network = data_controller.get_network(wiki, network_code, lower, upper)

        df = network.get_metric_dataframe(metric)

        # check the col to sort
        if sort_set and sort_set[0]['column_id'] in list(df):
            df = df.sort_values(sort_set[0]['column_id'],
                ascending=sort_set[0]['direction'] == 'asc',
                inplace=False)
        else:
            df = df.sort_values(metric, ascending=False)

        return df.iloc[
                pag_set['current_page']*pag_set['page_size']:
                (pag_set['current_page'] + 1)*pag_set['page_size']
            ].to_dict('rows')


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
        step = int(step)

        if bt_back and int(bt_back) > int(bt_forward):
            step = -step
        elif not (bt_forward and int(bt_forward) > int(bt_back)):
            raise PreventUpdate()

        # step value is in [0, n] | n € N
        # so step value must be a positive value if bt_forward was press

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
        Output('user-info', 'children'),
        [Input('cytoscape', 'tapNodeData')],
        [State('initial-selection', 'children')]
    )
    def update_node_info(user_info, selection_json):
        if not user_info:
            raise PreventUpdate()

        selection = json.loads(selection_json)
        network_code = selection['network']
        dic_info = net_factory.get_user_info(network_code)
        dic_metrics = net_factory.get_available_metrics(network_code)

        info_stack = []
        # Let's add the user info
        for key in dic_info.keys():
            if dic_info[key] in user_info:
                info_stack.append(html.P(f'{key}: {user_info[dic_info[key]]}'))

        # Let's add the metrics
        for key in dic_metrics.keys():
            if dic_metrics[key] in user_info:
                info_stack.append(html.P(f'{key}: {user_info[dic_metrics[key]]}'))

        return info_stack


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
