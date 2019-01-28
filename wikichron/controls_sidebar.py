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


def stats():
    return html.Div([
            html.H5('Network Stats', className='control-title'),
            html.Div(id='stats', className='stats-container',
                children=[
                    html.Div([
                        html.P('Nodes: ...', className='left-element'),
                        html.P('First User: ...', className='right-element')
                    ]),
                    html.Div([
                        html.P('Edges: ...', className='left-element'),
                        html.P('Last User: ...', className='right-element')
                    ]),
                    html.Div([
                        html.P('Communities: ...', className='left-element', id='n_communities'),
                        html.P('Max Hub Degree: ...', className='right-element')
                    ])
                ]),
        ], className='control-container')


def metrics():
    return html.Div([
            html.H5('Network Metrics', className='control-title'),
            html.Div(children=[
                html.Div(children=[
                    html.Span('PageRank', className='left-element'),
                    html.Button('Run', id='calculate_page_rank',
                        className='right-element button-off'),
                    ], className='metrics-section'),
                html.Div([
                    html.Span('Communities', className='left-element'),
                    html.Button('Run', id='calculate_communities',
                        className='right-element button-off')
                ], className='metrics-section')
            ])
        ], className='control-container')


def controls():
    return html.Div([
            html.H5('Network Controls', className='control-title'),
            html.Div([
                    html.Button('Show Labels', id='show_labels', 
                        className='control-button button-off'),
                    html.Button('Show PageRank', id='show_page_rank', 
                        className='control-button button-off'),
                    html.Button('Color by Cluster', id='color_cluster', 
                        className='control-button button-off'),
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
                                    stats(),
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
        date1 = datetime.fromtimestamp(cy_network["oldest_user"]).strftime("%Y-%m-%d")
        date2 = datetime.fromtimestamp(cy_network["newest_user"]).strftime("%Y-%m-%d")
        return [
                html.Div([
                        html.P(f'Nodes: {cy_network["num_nodes"]}', className='left-element'),
                        html.P(f'First User: {date1}', className='right-element')
                    ]),
                html.Div([
                        html.P(f'Edges: {cy_network["num_edges"]}', className='left-element'),
                        html.P(f'Last User: {date2}', className='right-element')
                    ]),
                html.Div([
                        html.P(f'Communities: {cy_network["n_communities"]}', 
                            className='left-element', id='n_communities'),
                        html.P(f'Max Hub Degree: {cy_network["max_degree"]}', 
                            className='right-element')
                    ])
            ]

    @app.callback(
        Output('show_labels', 'className'),
        [Input('show_labels', 'n_clicks')]
    )
    def switch_show_labels(clicks):
        if not clicks or clicks % 2 == 0:
            return 'control-button button-off'
        return 'control-button button-on'

    @app.callback(
        Output('show_page_rank', 'className'),
        [Input('show_page_rank', 'n_clicks')]
    )
    def switch_show_page_rank(clicks):
        if not clicks or clicks % 2 == 0:
            return 'control-button button-off'
        return 'control-button button-on'

    @app.callback(
        Output('calculate_page_rank', 'className'),
        [Input('calculate_page_rank', 'n_clicks')]
    )
    def switch_run_page_rank(clicks):
        if not clicks or clicks % 2 == 0:
            return 'right-element button-off'
        return 'right-element button-on'

    @app.callback(
        Output('color_cluster', 'className'),
        [Input('color_cluster', 'n_clicks')]
    )
    def switch_color_by_cluster(clicks):
        if not clicks or clicks % 2 == 0:
            return 'control-button button-off'
        return 'control-button button-on'

    @app.callback(
        Output('calculate_communities', 'className'),
        [Input('calculate_communities', 'n_clicks')]
    )
    def switch_run_communities(clicks):
        if not clicks or clicks % 2 == 0:
            return 'right-element button-off'
        return 'right-element button-on'

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