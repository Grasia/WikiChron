#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   controls_sidebar.py

   Descp: Another sidebar, positioned in the right side, to display the user
      controls for WikiChron.

   Created on: 11-dic-2018

   Copyright 2018 Youssef 'FRYoussef' El Faqir el Rhazoui <f.r.youssef@hotmail.com>
   Copyright 2018 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""
import dash
import dash_core_components as dcc
import grasia_dash_components as gdc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from datetime import datetime


def fold_button():
    return html.Div(
        html.Div(
            id='controls-fold-img-container',
            className='fold-img-container-cn',
            children=[
                html.P(id='controls-fold-button', className='fold-button-cn')
            ],
        ),
        id='controls-fold-container',
        style={
            'display': 'flex'
        }
    );

def stats_section():
    return html.Div([
            html.H5('Network Stats', className='control-title'),
            html.Div(id='stats', className='stats-container', children=stats())
            ], className='control-container')

def stats(stat1 = 'Nodes: ...', stat2 = 'First User: ...', stat3 = 'Edges: ...',
        stat4 = 'Last User: ...', stat5 = 'Communities: ...',
        stat6 = 'Max Hub Degree: ...'):

    return [
            html.Div([
                html.P(stat1, className='left-element'),
                html.P(stat2, className='right-element')
            ]),
            html.Div([
                html.P(stat3, className='left-element'),
                html.P(stat4, className='right-element')
            ]),
            html.Div([
                html.P(stat5, className='left-element', id='n_communities'),
                html.P(stat6, className='right-element')
            ])]


def metrics():
    return html.Div([
            html.H5('Network Metrics', className='control-title'),
            html.Div(children=[
                html.Div(children=[
                    html.Span('PageRank', className='left-element'),
                    html.Button('Run', id='calculate_page_rank',
                                type='button',
                                className='right-element action-button'),
                    ],
                    className='metrics-section'),
                html.Div([
                    html.Span('Communities', className='left-element'),
                    html.Button('Run', id='calculate_communities',
                                type='button',
                                className='right-element action-button')
                ],
                className='metrics-section')
            ])
        ], className='control-container')


def controls():
    return html.Div([
            html.H5('Network Controls', className='control-title'),
            html.Div([
                    html.Button('Show Labels', id='show_labels',
                        className='control-button action-button'),
                    html.Button('Show PageRank', id='show_page_rank',
                        disabled=True,
                        className='control-button action-button'),
                    html.Button('Color by Cluster', id='color_cluster',
                        disabled=True,
                        className='control-button action-button'),
                ])
        ], className='control-container')


def generate_controls_sidebar():
    return html.Div(id='controls-sidebar-wrapper',
                children=[
                    html.Div(id='controls-side-bar',
                        className='side-bar-cn',
                        children=[
                            fold_button(),
                            html.Div(id='controls-side-bar-content',
                                children=[
                                    stats_section(),
                                    metrics(),
                                    controls()
                                ]),
                            gdc.Import(src='js/controls_side_bar.js')
                        ])
                ],
                style={
                    'display': 'flex',
                    'flexDirection': 'row-reverse'
                }

    );


def bind_control_callbacks(app):
    
    @app.callback(
        Output('stats', 'children'),
        [Input('network-ready', 'value')]
    )
    def update_stats(cy_network):
        if not cy_network:
            return stats()

        date1 = datetime.fromtimestamp(cy_network["oldest_user"]).strftime("%Y-%m-%d")
        date2 = datetime.fromtimestamp(cy_network["newest_user"]).strftime("%Y-%m-%d")

        return stats(stat1 = f'Nodes: {cy_network["num_nodes"]}', stat2 = f'First User: {date1}',
            stat3 = f'Edges: {cy_network["num_edges"]}', stat4 = f'Last User: {date2}',
            stat5 = f'Communities: {cy_network["n_communities"]}',
            stat6 = f'Max Hub Degree: {cy_network["max_degree"]}')


    @app.callback(
        Output('show_labels', 'className'),
        [Input('show_labels', 'n_clicks')]
    )
    def switch_show_labels(clicks):
        if not clicks or clicks % 2 == 0:
            return 'control-button action-button'
        return 'control-button action-button-pressed'


    @app.callback(
        Output('show_page_rank', 'className'),
        [Input('show_page_rank', 'n_clicks')]
    )
    def switch_show_page_rank(clicks):
        if not clicks or clicks % 2 == 0:
            return 'control-button action-button'
        return 'control-button action-button-pressed'


    @app.callback(
        Output('color_cluster', 'className'),
        [Input('color_cluster', 'n_clicks')]
    )
    def switch_color_by_cluster(clicks):
        if not clicks or clicks % 2 == 0:
            return 'control-button action-button'
        return 'control-button action-button-pressed'


    @app.callback(
        Output('calculate_page_rank', 'className'),
        [Input('calculate_page_rank', 'n_clicks')]
    )
    def switch_run_page_rank(clicks):
        if not clicks:
            return 'right-element action-button'
        return 'right-element action-button-pressed'


    @app.callback(
        Output('calculate_communities', 'className'),
        [Input('calculate_communities', 'n_clicks')]
    )
    def switch_run_communities(clicks):
        if not clicks:
            return 'right-element action-button'
        return 'right-element action-button-pressed'


    @app.callback(
        Output('calculate_page_rank', 'disabled'),
        [Input('calculate_page_rank', 'n_clicks')]
    )
    def disable_button_run_page_rank(clicks):
        if not clicks:
            return False
        return True


    @app.callback(
        Output('calculate_communities', 'disabled'),
        [Input('calculate_communities', 'n_clicks')]
    )
    def disable_button_run_communities(clicks):
        if not clicks:
            return False
        return True


    @app.callback(
        Output('show_page_rank', 'disabled'),
        [Input('calculate_page_rank', 'n_clicks')]
    )
    def disable_toggle_show_page_rank(clicks):
        if not clicks:
            return True
        return False


    @app.callback(
        Output('color_cluster', 'disabled'),
        [Input('calculate_communities', 'n_clicks')]
    )
    def disable_toggle_show_communities(clicks):
        if not clicks:
            return True
        return False


    @app.callback(
        Output('n_communities', 'content'),
        [Input('calculate_communities', 'n_clicks')],
        [State('network-ready', 'value')]
    )
    def show_num_communities(_, cy_network):
        return f'Communities: {cy_network["n_communities"]}'


if __name__ == '__main__':
    print('Using version ' + dcc.__version__ + ' of Dash Core Components.')
    print('Using version ' + gdc.__version__ + ' of Grasia Dash Components.')

    global app;

    app = dash.Dash()

    app.scripts.config.serve_locally = True

    #~ app.scripts.append_script({ "external_url": "app.js"})

    app.layout = html.Div(id='app-layout',
        style={'display': 'flex'},
        children=[
            html.Div(id='main',
                    className='control-text',
                    style={'width': '100%'},
                    children=[
                        generate_controls_sidebar()
                    ])
        ]
    );

    #~ bind_callbacks(app)

    app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
    app.css.append_css({"external_url": "https://codepen.io/akronix/pen/rpQgqQ.css"})

    app.run_server(port=8054, debug=True)
