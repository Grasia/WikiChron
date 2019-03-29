"""
    right_side_bar.py

    Descp: This file is gonna be use to implement the new app design,
    thus it'll warp the side components

    Created on: 26/03/2019

    Copyright 2019 Youssef 'FRYoussef' El Faqir el Rhazoui
        <f.r.youssef@hotmail.com>
"""

import time
import json
from datetime import datetime
import os

import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from . import data_controller
from .networks.models.BaseNetwork import BaseNetwork
from .networks.models import networks_generator as net_factory

global debug
debug = True if os.environ.get('FLASK_ENV') == 'development' else False


def build_sidebar(network_code) -> html.Div:
    """
    Use this function in order to build and get the side elements
    """
    return html.Div(className='', children=[
        build_network_stats(list(BaseNetwork.get_network_stats().keys())),
        build_table(network_code),
        build_user_stats()
        ])


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
            dcc.Dropdown(
                id='dd-local-metric',
                options=options,
                placeholder='Select a local metric'
            ),
            dash_table.DataTable(
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
            )], className='body-pane')
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


def bind_sidebar_callbacks(app):

        @app.callback(
            Output('net-stats', 'children'),
            [Input('network-ready', 'value')]
        )
        def update_network_stats(cy_network):
            if not cy_network:
                raise PreventUpdate()

            stats = BaseNetwork.get_network_stats()
            child = []
            i = 0
            group = []
            for k, val in stats.items():
                group.append(html.Div(children=[
                    html.P(f'{k}:'),
                    html.P(cy_network[val])
                ]))

                i += 1
                if i % 2 == 0:
                    child.append(html.Div(children=group))
                    group = []

            return child


        @app.callback(
            Output('ranking-table', 'columns'),
            [Input('dd-local-metric', 'value')],
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
            Input('dd-local-metric', 'value'),
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
            elif not df.empty:
                df = df.sort_values(metric, ascending=False)
            else:
                return []

            return df.iloc[
                    pag_set['current_page']*pag_set['page_size']:
                    (pag_set['current_page'] + 1)*pag_set['page_size']
                ].to_dict('rows')


        @app.callback(
            Output('user-stats', 'children'),
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
                    info_stack.append(html.Div(children=[
                        html.P(f'{key}:'),
                        html.P(user_info[dic_info[key]])
                    ], className='user-container-stat'))

            # Let's add the metrics
            for key in dic_metrics.keys():
                if dic_metrics[key] in user_info:
                    info_stack.append(html.Div(children=[
                        html.P(f'{key}:'),
                        html.P(user_info[dic_metrics[key]])
                    ], className='user-container-stat'))

            return info_stack


        # @app.callback(
        #     Output('metric-to-show', 'value'),
        #     [Input('dd-local-metric', 'value')],
        #     [State('network-ready', 'value'),
        #     State('initial-selection', 'children')]
        # )
        # def select_metric(dd_val, ready, selection_json):
        #     if not ready:
        #         raise PreventUpdate()

        #     selection = json.loads(selection_json)
        #     network_code = selection['network']

        #     tms = [int(tm_edits), int(tm_bet), int(tm_pr)]
        #     metrics = net_factory.get_available_metrics(network_code).keys()
        #     tm_metrics = {key:value for key, value in zip(tms, metrics)}
        #     max_key = max(tm_metrics, key=int)
        #     return tm_metrics[max_key]