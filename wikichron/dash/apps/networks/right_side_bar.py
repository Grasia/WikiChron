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

from .networks.models.BaseNetwork import BaseNetwork

global debug
debug = True if os.environ.get('FLASK_ENV') == 'development' else False


def build_sidebar() -> html.Div:
    """
    Use this function in order to build and get the side elements
    """
    return html.Div(className='', children=[
        build_network_stats(list(BaseNetwork.get_network_stats().keys())),
        build_table(),
        build_user_stats()
        ])


def build_network_stats(stats: list()) -> html.Div:
    header = html.Div(children='Network Stats', className='header-pane')
    body = html.Div(children=[
            html.Div([
                html.P(f'{stats[0]}: ...'),
                html.P(f'{stats[1]}: ...')
            ]),
            html.Div([
                html.P(f'{stats[2]}: ...'),
                html.P(f'{stats[3]}: ...')
            ])], className='body-pane')

    return html.Div(children=[header, body], className='side-pane')


def build_table() -> html.Div:
    header = html.Div(children='Ranking', className='header-pane')
    body = html.Div(children=[
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
    return html.Div(children=[header, body], className='side-pane')


def build_user_stats() -> html.Div:
    header = html.Div(children='User Stats', className='header-pane')
    body = html.Div(id='user-stats', children='Click a node', className='body-pane')
    return html.Div(children=[header, body], className='side-pane')


def bind_sidebar_callbacks(app):
    pass