#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   side_bar.py

   Descp:

   Created on: 25-oct-2017

   Copyright 2017 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import grasia_dash_components as gdc
import dash_html_components as html

global app;

def fold_button():
    return html.Div(
        html.Div(
            id='fold-img-container',
            style={
                'cursor': 'pointer',
                'marginRight': '23px',
                'marginTop': '30px',
                'marginBotton': '30px'
            },
            children=[html.Img(id='fold-img', src='assets/fold_arrow.svg')],
        ),
        id='fold-container',
        style={
            'display': 'flex',
            'flexDirection': 'row-reverse'
        }
    );

def wikis_tab():
    return html.Div([
        html.Div(
            children=[
                html.P(html.Strong('You can compare between 3 wikis')),
                html.Div(
                    id='category-1',
                    className='aside-category',
                    children=[
                        html.H3('Category 1'),
                        html.Img(src='assets/ico_minus.svg')
                    ],
                    style= {
                        'display': 'flex',
                        'justify-content': 'space-between'
                    }
                ),
                dcc.Checklist(
                    className='aside-checklist-category',
                    options=[
                        {'label': 'Wiki 1', 'value': '1'},
                        {'label': 'Wiki 2', 'value': '2'},
                        {'label': 'Wikipedia', 'value': '3'},
                        {'label': 'Wiki 4', 'value': '4'},
                        {'label': 'Wiki 5', 'value': '5'},
                        {'label': 'Wiki 6', 'value': '6'}
                    ],
                    values=['3,4,5'],
                    labelClassName='aside-checklist-option',
                    labelStyle={'display': 'block'}
                ),
            ],
            style={'color': 'white'},
            className='container',
            id='wikis-tab-container'
            ),
        ],
        id='wikis-tab'
    );

def metrics_tab(metrics):

    metrics_options = [{'label': metric.text, 'value': metric.code} for metric in metrics]

    return html.Div([
        html.Div(
            children=[
                html.P(html.Strong('Please, select the charts you wish to see and when you finish click on compare')),
                dcc.Checklist(
                            className='aside-checklist-category',
                            options=metrics_options,
                            values=[],
                            labelClassName='aside-checklist-option',
                            labelStyle={'display': 'block'}
                        )
                #~ gdc.Accordion(
                    #~ id='pages-metric',
                    #~ className='aside-category',
                    #~ label='Pages',
                    #~ children=[
                        #~ dcc.Checklist(
                            #~ className='aside-checklist-category',
                            #~ options=metrics_options,
                            #~ values=[],
                            #~ labelClassName='aside-checklist-option',
                            #~ labelStyle={'display': 'block'}
                        #~ )
                    #~ ]
                #~ )
            ],
            className='container',
            style={'color': 'white'},
            id='metrics-tab-container',
            ),
        compare_button()
        ],
        id='metrics-tab'
    );

def compare_button():
    buttonStyle = {
                    'border': 'None',
                    'height': '57px',
                    'width': '256px',
                    'borderRadius': '4px',
                    'backgroundColor': '#49A5E6',
                    'color' : 'white',
                    'fontFamily': 'Roboto',
                    'fontSize': '24px',
                    'fontWeight': 'bold',
                    'lineHeight': '28px',
                }

    return (
        html.Div(
            html.Button('COMPARE',
                        id='compare-button',
                        style= buttonStyle
            ),
            style = {
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'height': '80px'
            }
        )
    )

def generate_side_bar(metrics):
    return html.Div(id='side-bar',
        style={'backgroundColor': '#004481', 'width': '280px', 'height': '100%'},
        children=[
            fold_button(),
            dcc.Tabs(
                tabs=[
                    {'value': 'wikis', 'label': 'WIKIS'},
                    {'value': 'metrics', 'label': 'METRICS'}
                ],
                value='metrics',
                id='side-bar-tabs',
                vertical=False,
                style={
                    'width': '100%',
                    'textAlign': 'center',
                    'border': 'none',
                },
                tabsStyle={
                    'width': '50%',
                    'height': '70px',
                    'borderRadius': '3px',
                    'backgroundColor': '#004481',
                    'color': 'white',
                    'borderStyle': 'none',
                    'fontSize': '18px',
                    'lineHeight': '21px',
                    'justifyContent': 'center',
                    'flexDirection': 'column'
                }),
            wikis_tab(),
            metrics_tab(metrics),
        ]
    );


def bind_callbacks(app):

    @app.callback(Output('wikis-tab', 'style'),
                   [Input('side-bar-tabs', 'value')])
    def update_wikis_tab_visible(tab_selection):
        if tab_selection == 'wikis':
            return {'display':'block'}
        else:
            return {'display':'none'}

    @app.callback(Output('metrics-tab', 'style'),
               [Input('side-bar-tabs', 'value')])
    def update_metrics_tab_visible(tab_selection):
        if tab_selection == 'metrics':
            return {'display':'block'}
        else:
            return {'display':'none'}

    return


if __name__ == '__main__':

    print('Using version ' + dcc.__version__ + ' of Dash Core Components.')
    print('Using version ' + gdc.__version__ + ' of Grasia Dash Components.')

    global app;

    app = dash.Dash()

    app.scripts.config.serve_locally = True

    def start_image_server():
        import flask
        import glob
        import os

        static_image_route = '/assets/'
        image_directory = os.path.dirname(os.path.realpath(__file__)) + static_image_route
        list_of_images = [os.path.basename(x) for x in glob.glob('{}*.svg'.format(image_directory))]

        # Add a static image route that serves images from desktop
        # Be *very* careful here - you don't want to serve arbitrary files
        # from your computer or server
        @app.server.route('{}<image_path>.svg'.format(static_image_route))
        def serve_image(image_path):
            image_name = '{}.svg'.format(image_path)
            if image_name not in list_of_images:
                raise Exception('"{}" is excluded from the allowed static files'.format(image_path))
            return flask.send_from_directory(image_directory, image_name)

    start_image_server()

#~ app.scripts.append_script({ "external_url": "app.js"})

    from lib.interface import get_available_metrics
    app.layout = generate_side_bar(get_available_metrics())
    bind_callbacks(app)

    app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
    app.run_server(port=8052, debug=True)

