#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   CoEditingControlsSidebarDecorator.py

   Descp: A class to implement the decorator pattern in order to make an
     easier implementation of the right sidebar

   Created on: 08-02-2019

   Copyright 2019 Youssef 'FRYoussef' El Faqir el Rhazoui <f.r.youssef@hotmail.com>
"""

import time
import json
from datetime import datetime
import os

import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from .BaseControlsSidebarDecorator import BaseControlsSidebarDecorator
from networks.CytoscapeStylesheet import CytoscapeStylesheet
from networks.models.CoEditingNetwork import CoEditingNetwork
import data_controller
import networks.models.networks_generator as net_factory

global debug
debug = True if os.environ.get('FLASK_ENV') == 'development' else False

class CoEditingControlsSidebarDecorator(BaseControlsSidebarDecorator):

    def __init__(self, sidebar):
        super().__init__(sidebar)


    @staticmethod
    def default_stats(st1 = 'Nodes: ...', st2 = 'Edges: ...', 
            st3 = 'Assortativity Degree: ...', st4 = 'Communities: ...',):

        return [
                html.Div([
                    html.P(st1, className='left-element'),
                    html.P(st2, className='right-element')
                ]),
                html.Div([
                    html.P(st3, className='left-element'),
                    html.P(st4, className='right-element')
                ])]


    @staticmethod
    def default_options():
        return [
                    html.Button('Show Labels', id='show-labels',
                        className='control-button action-button',
                        n_clicks_timestamp='0'),
                    html.Button('Show Edits', id='show-edits',
                        className='control-button action-button',
                        n_clicks_timestamp='1'),
                    html.Button('Show PageRank', id='show-page-rank',
                        className='control-button action-button',
                        n_clicks_timestamp='2'),
                    html.Button('Show Betweenness', id='show-betweenness',
                        className='control-button action-button',
                        n_clicks_timestamp='3'),
                    html.Button('Color by Cluster', id='color-cluster',
                        className='control-button action-button',
                        n_clicks_timestamp='4'),
                ]


    def add_stats_section(self):
        stats = self.default_stats()
        super().add_stats_section(stats)


    def add_options_section(self):
        options = self.default_options()
        super().add_options_section(options)


    def add_all_sections(self):
        self.add_stats_section()
        self.add_options_section()


    @classmethod
    def bind_callbacks(cls, app):

        @app.callback(
            Output('stats', 'children'),
            [Input('network-ready', 'value')]
        )
        def update_stats(cy_network):
            if not cy_network:
                return CoEditingControlsSidebarDecorator.default_stats()

            return CoEditingControlsSidebarDecorator.default_stats(
                st1 = f'Nodes: {cy_network["num_nodes"]}',
                st2 = f'Edges: {cy_network["num_edges"]}',
                st3 = f'Assortativity Degree: {cy_network["assortativity_degree"]}',
                st4 = f'Communities: {cy_network["n_communities"]}'
                )


        @app.callback(
            Output('show-labels', 'className'),
            [Input('show-labels', 'n_clicks')]
        )
        def switch_show_labels(clicks):
            if not clicks or clicks % 2 == 0:
                return 'control-button action-button'
            return 'control-button action-button-pressed'


        @app.callback(
            Output('color-cluster', 'className'),
            [Input('color-cluster', 'n_clicks')]
        )
        def switch_color_by_cluster(clicks):
            if not clicks or clicks % 2 == 0:
                return 'control-button action-button'
            return 'control-button action-button-pressed'


        @app.callback(
            Output('cytoscape', 'stylesheet'),
            [Input('cytoscape', 'elements'),
            Input('show-labels', 'n_clicks'),
            Input('color-cluster', 'n_clicks'),
            Input('highlight-node', 'value'),
            Input('dd-color-metric', 'value')],
            [State('network-ready', 'value'),
            State('initial-selection', 'children')]
        )
        def update_stylesheet(_, lb_clicks, com_clicks, nodes_selc, dd_val, 
            cy_network, selection_json):

            if not cy_network:
                raise PreventUpdate()

            selection = json.loads(selection_json)
            network_code = selection['network']

            stylesheet = CytoscapeStylesheet()
            metric = {}

            if dd_val:
                metric = net_factory.get_secondary_metrics(network_code)[dd_val]

            if not nodes_selc:
                stylesheet.all_transformations(cy_network, metric)
            else:
                stylesheet.highlight_nodes(cy_network, nodes_selc)

            if lb_clicks and lb_clicks % 2:
                stylesheet.set_label('label')
            else:
                stylesheet.set_label('')

            if com_clicks and com_clicks % 2 == 1:
                stylesheet.color_nodes_by_cluster()
            else:
                stylesheet.color_nodes(cy_network, metric)

            return stylesheet.cy_stylesheet


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
            Output('metric-to-show', 'value'),
            [Input('show-page-rank', 'n_clicks_timestamp'),
            Input('show-edits', 'n_clicks_timestamp'),
            Input('show-betweenness', 'n_clicks_timestamp')],
            [State('network-ready', 'value'),
            State('initial-selection', 'children')]
        )
        def select_metric(tm_pr, tm_edits, tm_bet, ready, selection_json):
            if not ready:
                raise PreventUpdate()

            selection = json.loads(selection_json)
            network_code = selection['network']

            tms = [int(tm_edits), int(tm_bet), int(tm_pr)]
            metrics = net_factory.get_available_metrics(network_code).keys()
            tm_metrics = {key:value for key, value in zip(tms, metrics)}
            max_key = max(tm_metrics, key=int)
            return tm_metrics[max_key]