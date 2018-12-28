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
        className= 'fold-control-side',
        style={
            'display': 'flex'
        }
    );

def stats():
    return html.Div([
            html.H5('Network Stats', style={'text-align': 'center'}),
            html.Div(id='stats', className='stats-container',
                children=[
                    html.Div([
                        html.P('Nodes: ...', className='left-stats'),
                        html.P('First User: ...', className='right-stats')
                    ]),
                    html.Div([
                        html.P('Edges: ...', className='left-stats'),
                        html.P('Last User: ...', className='right-stats')
                    ])
                ]),
        ])

def generate_controls_sidebar():
    return html.Div(id='controls-sidebar-wrapper',
                children=[
                    html.Div(id='controls-side-bar',
                        className='side-bar-cn',
                        children=[
                            fold_button(),
                            html.Div(id='controls-side-bar-content', children=[stats()], 
                                className='control-container'),
                            gdc.Import(src='js/controls_side_bar.js')
                        ])
                ],
                style={
                    'display': 'flex',
                    'flexDirection': 'row-reverse'
                }

    );


# def bind_callbacks(app):

#     @app.callback(
#         Output('stats', 'children'),
#         [Input('network-ready', 'value')]
#     )
#     def update_stats(network):
#         return [
#                 html.Div([
#                         html.P(f'Nodes: {network["num_nodes"]}', className='left-stats'),
#                         html.P(f'Edges: {network["num_edges"]}', className='right-stats')
#                     ]),
#                 html.Div([
#                         html.P(f'First User: {network["oldest_user"]}', className='left-stats'),
#                         html.P(f'Last User: {network["newest_user"]}', className='right-stats')
#                     ])
#             ]


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