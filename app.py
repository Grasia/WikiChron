#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   app.py

   Descp:

   Created on: 23-oct-2017

   Copyright 2017 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""
import flask
import glob
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from tabs_bar import generate_tabs_bar
from main import generate_main_content
import side_bar

# Local imports:
import lib.interface as lib

port = 8888
global app;
app = dash.Dash()

app.scripts.config.serve_locally = True

app.scripts.append_script({
    "external_url": "app.js"
})

#~ app.css.config.serve_locally = True

#~ app.css.append_css({'external_url': 'dash.css'})
#~ app.css.append_css({'external_url': 'app.css'})
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
#~ app.css.append_css({"external_url": "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css"})

tabs = [
    {'value': 1, 'icon': 'assets/white_graphic.svg'},
    {'value': 2, 'icon': 'assets/white_graphic.svg'},
    {'value': 3, 'icon': 'assets/white_graphic.svg'},
    {'value': 4, 'icon': 'assets/white_graphic.svg'},
]

wikis = ['eslagunanegra_pages_full', 'cocktails', 'zelda']
available_metrics = lib.get_available_metrics()

def set_layout():
    app.layout = html.Div(id='app-layout',
        style={'display': 'flex'},
        children=[
            generate_tabs_bar(tabs),
            side_bar.generate_side_bar(wikis, available_metrics),
            #~ generate_main_content()
        ]
    );
    return

def start_css_server():
    # Add a static styles route that serves css from desktop
    # Be *very* careful here - you don't want to serve arbitrary files
    # from your computer or server
    static_css_route = '/styles/'
    css_directory = os.path.dirname(os.path.realpath(__file__)) + static_css_route
    stylesheets = ['app.css']

    @app.server.route('{}<css_path>.css'.format(static_css_route))
    def serve_stylesheet(css_path):
        css_name = '{}.css'.format(css_path)
        if css_name not in stylesheets:
            raise Exception(
                '"{}" is excluded from the allowed static files'.format(
                    css_path
                )
            )
        print (stylesheet)
        print (css_name)
        return flask.send_from_directory(css_directory, css_name)


    for stylesheet in stylesheets:
        app.css.append_css({"external_url": "/styles/{}".format(stylesheet)})


def start_image_server():

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


if __name__ == '__main__':
    print('Using version ' + dcc.__version__ + ' of Dash Core Components.')

    start_image_server()
    start_css_server()

    set_layout()
    side_bar.bind_callbacks(app)

    app.run_server(debug=True, port=port)
