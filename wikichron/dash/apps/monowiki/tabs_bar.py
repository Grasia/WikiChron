#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   tabs_bar.py

   Descp:

   Created on: 24-oct-2017

   Copyright 2017-2018 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import grasia_dash_components as gdc
import dash_html_components as html

def generate_tabs_bar(tabs):
    return html.Div([
        gdc.Tabs(
            tabs=tabs,
            value=1,
            id='tabs',
            vertical=True,
            style={
                'height': '100vh',
                'textAlign': 'left',
                'flex': '0 0 75px',
                'backgroundColor': '#072146',
                'border': 'none'
            },
            tabsStyle={
                'backgroundColor': '#004481',
                'color': 'white',
                'margin': '5px',
                'borderStyle': 'none'
            }
        ),
    ],
    id='tabs-bar',
    style={
        'fontFamily': 'Sans-Serif'
    })


if __name__ == '__main__':

    print('Using version ' + dcc.__version__ + ' of Dash Core Components.')

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

    tabs=[
        {'value': 1, 'label': 'test', 'icon': 'assets/white_graphic.svg'},
        {'value': 2, 'label': 'Tab 2'},
        {'value': 3, 'icon': 'assets/white_graphic.svg'},
        {'value': 4, 'icon': 'assets/white_graphic.svg'},
    ]
    app.layout = generate_tabs_bar(tabs)


    app.run_server(port=8051, debug=True)
