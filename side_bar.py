#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   side_bar.py

   Descp:

   Created on: 25-oct-2017

   Copyright 2017 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

import json
import os

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import grasia_dash_components as gdc
import dash_html_components as html

global app;

global debug;
debug = 'DEBUG' in os.environ

def fold_button():
    return html.Div(
        html.Div(
            id='fold-img-container',
            style={
                'cursor': 'pointer',
                'marginRight': '23px',
                'marginTop': '30px',
                'marginBottom': '30px'
            },
            children=[html.Img(id='fold-img', src='assets/fold_arrow.svg')],
        ),
        id='fold-container',
        style={
            'display': 'flex',
            'flexDirection': 'row-reverse'
        }
    );

def wikis_tab(wikis):

    wikis_options = [{'label': wiki, 'value': wiki} for wiki in wikis]

    return html.Div([
        html.Div(
            children=[
                html.P(
                    html.Strong(('You can compare between {} wikis').format(len(wikis))),
                    className="sidebar-info-paragraph"
                    ),
                #~ html.Div(
                    #~ id='category-1',
                    #~ className='aside-category',
                    #~ children=[
                        #~ html.H3('Category 1'),
                        #~ html.Img(src='assets/ico_minus.svg')
                    #~ ],
                    #~ style= {
                        #~ 'display': 'flex',
                        #~ 'justify-content': 'space-between'
                    #~ }
                #~ ),
                dcc.Checklist(
                    id='wikis-checklist-selection',
                    className='aside-checklist-category',
                    options=wikis_options,
                    values=[],
                    labelClassName='aside-checklist-option',
                    labelStyle={'display': 'block'}
                ),
            ],
            style={'color': 'white'},
            className='container',
            id='wikis-tab-container'
            ),
        html.Hr(),
        compare_button()
        ],
        id='wikis-tab'
    );

def select_time_axis_control():
    return (html.Div([
        html.Hr(),
        html.Div([
            dcc.RadioItems(
                options=[
                    {'label': 'Relative dates', 'value': 'relative'},
                    {'label': 'Absolute dates', 'value': 'absolute'}
                ],
                value='relative',
                id='time-axis-selection'
            ),
            ],
            className="container"
        ),
        html.Hr()
        ])
    )

def metrics_tab(metrics):

    def group_metrics_in_accordion(metrics, metric_category):

        metrics_options = [{'label': metric.text, 'value': metric.code} for metric in metrics]

        return gdc.Accordion(
                    id='{}-metrics'.format(metric_category.name),
                    className='aside-category',
                    label=metric_category.value,
                    itemClassName='metric-category-label',
                    childrenClassName='metric-category-list',
                    accordionFixedWidth='300',
                    defaultCollapsed=True,
                    children=[
                        dcc.Checklist(
                            id='metrics-checklist-selection',
                            className='aside-checklist-category',
                            options=metrics_options,
                            values=[],
                            labelClassName='aside-checklist-option',
                            labelStyle={'display': 'block'}
                        )
                    ],
                    style={'display': 'block'}
                )


    #~ metrics_options = [{'label': metric.text, 'value': metric.code} for metric in metrics]

    metrics_by_category = {}

    for metric in metrics:
        if metric.category not in metrics_by_category:
            metrics_by_category[metric.category] = [metric]
        else:
            metrics_by_category[metric.category].append(metric)

    metrics_checklist = []
    for category, metrics_categorized in metrics_by_category.items():
        metrics_checklist.append(group_metrics_in_accordion(metrics_categorized, category))

    #~ for metric_category in metric_categories:
        #~ metrics_with_this_category = [metric for metric in metrics if metric.category.name == metric_category ]
        #~ metrics_by_category.append(group_metrics_in_accordion(metrics_with_this_category, metric_category))

    intro_metrics_paragraph = html.Div(
                html.P(
                    html.Strong('Please, select the charts you wish to see and when you finish click on compare'),
                    className="sidebar-info-paragraph"
                ),
                className="container")

    return html.Div([
        html.Div(
            children = [intro_metrics_paragraph] + metrics_checklist,
                #~ dcc.Checklist(
                            #~ id='metrics-checklist-selection',
                            #~ className='aside-checklist-category',
                            #~ options=metrics_options,
                            #~ values=[],
                            #~ labelClassName='aside-checklist-option',
                            #~ labelStyle={'display': 'block'}
                        #~ ),
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
            style={'color': 'white'},
            id='metrics-tab-container',
            ),
        select_time_axis_control(),
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
                        style=buttonStyle,
                        n_clicks=0
            ),
            style = {
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'height': '80px'
            }
        )
    )

def selection_result_container():
    if debug:
        return html.Div(id='sidebar-selection', style={'display': 'block'})
    else:
        return html.Div(id='sidebar-selection', style={'display': 'none'})

def generate_side_bar(wikis, metrics):
    return html.Div(id='side-bar',
        children=[
            fold_button(),
            gdc.Tabs(
                tabs=[
                    {'value': 'wikis', 'label': 'WIKIS'},
                    {'value': 'metrics', 'label': 'METRICS'}
                ],
                value='wikis',
                id='side-bar-tabs',
                vertical=False,
                selectedTabStyle={
                    'backgroundColor': '#004481',
                },
                style={
                    'width': '100%',
                    'textAlign': 'center',
                    'border': 'none',
                },
                tabsStyle={
                    'width': '50%',
                    'height': '70px',
                    'borderRadius': '3px',
                    'backgroundColor': '#072146',
                    'color': 'white',
                    'borderLeftStyle': 'none',
                    'borderRightStyle': 'none',
                    'fontSize': '18px',
                    'lineHeight': '21px',
                    'justifyContent': 'center',
                    'flexDirection': 'column'
                }),
            wikis_tab(wikis),
            metrics_tab(metrics),
            selection_result_container()
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

    @app.callback(Output('sidebar-selection', 'children'),
               [Input('compare-button', 'n_clicks')],
               [State('wikis-checklist-selection', 'values'),
               State('metrics-checklist-selection', 'values'),
               State('time-axis-selection', 'value'),
               ]
               )
    def compare_selection(n_clicks, wikis_selection, metrics_selection, time_axis_selection):
        print('Number of clicks: ' + str(n_clicks))
        if (n_clicks > 0 ):
            selection = { 'wikis': wikis_selection, 'metrics': metrics_selection, 'time': time_axis_selection}
            return json.dumps(selection)

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
    example_wikis = ['eslagunanegra_pages_full', 'cocktails', 'zelda']
    app.layout = generate_side_bar(example_wikis, get_available_metrics())
    bind_callbacks(app)

    app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
    app.run_server(port=8052, debug=True)

