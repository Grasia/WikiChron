#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   main.py

   Descp: Generate the main content of the webapp:
Title, plots and filter elements.

   Created on: 01-nov-2017

   Copyright 2017-2018 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

import os
import time
from warnings import warn
import json
from urllib.parse import urlencode

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output, State
import grasia_dash_components as gdc
import sd_material_ui
from flask import current_app

# Local imports:
from .metrics import interface as interface
from .utils import get_mode_config
from . import data_controller

global debug
debug = True if os.environ.get('FLASK_ENV') == 'development' else False


def extract_metrics_objs_from_metrics_codes(metric_codes):
    metrics_dict = interface.get_available_metrics_dict()
    metrics = [ metrics_dict[metric] for metric in metric_codes ]
    return metrics


def generate_graphs(data, metrics, wikis, relative_time):
    """ Turn over data[] into plotly graphs objects and store it in graphs[] """

    graphs_list = [[None for j in range(len(wikis))] for i in range(len(metrics))]

    for metric_idx in range(len(metrics)):
        for wiki_idx in range(len(wikis)):
            metric_data = data[metric_idx][wiki_idx]
            if relative_time:
                x_axis = list(range(len(metric_data.index))) # relative to the age of the wiki in months
            else:
                x_axis = metric_data.index # natural months

            graphs_list[metric_idx][wiki_idx] = go.Scatter(
                                x=x_axis,
                                y=metric_data,
                                name=wikis[wiki_idx]['name']
                                )

    return graphs_list



def generate_main_content(wikis_arg, metrics_arg, relative_time_arg,
                            query_string):
    """
    It generates the main content
    Parameters:
        -wikis_arg: wikis to use
        -metrics_arg: metrics to apply to those wikis
        -relative_time_arg: Use relative or absolute time axis?
        -query_string: query string of the current selection

    Return: An HTML object with the main content
    """

    # Load app config
    server_config = current_app.config
    mode_config = get_mode_config(current_app)
    # Contructs the assets_url_path for image sources:
    assets_url_path = os.path.join(mode_config['DASH_STATIC_PATHNAME'], 'assets')


    def main_header():
        """
        Generates the main header

        Return: An HTML object with the header content
        """
        href_download_button = f'{mode_config["DASH_DOWNLOAD_PATHNAME"]}{query_string}'
        return (html.Div(id='header',
                className='main-root-header',
                children = [
                    html.Div(
                        id='header-container',
                        children=[
                            html.Div(
                                html.Img(src='{}/logo_compare_white.svg'.format(assets_url_path),
                                    id='title-img'),
                            ),
                            html.Hr(),
                            html.Div(
                                style={'display': 'flex', 'align-items': 'center', \
                                        'justify-content': 'space-between'},
                                children=[
                                    html.Div([
                                        html.Strong(
                                            html.A('< Go back to selection', href=selection_url)
                                        )
                                    ]),

                                    html.Div([
                                        html.A(
                                            html.Img(src='{}/share.svg'.format(assets_url_path)),
                                            id='share-button',
                                            className='icon',
                                            title='Share current selection'
                                        ),
                                        html.A(
                                            html.Img(src='{}/cloud_download.svg'.format(assets_url_path)),
                                            href=href_download_button,
                                            id='download-button',
                                            target='_blank',
                                            className='icon',
                                            title='Download data'
                                        ),
                                        html.A(
                                            html.Img(src='{}/documentation.svg'.format(assets_url_path)),
                                            href='https://github.com/Grasia/WikiChron/wiki/',
                                            target='_blank',
                                            className='icon',
                                            title='Documentation'
                                        ),
                                        html.A(
                                            html.Img(src='{}/ico-github.svg'.format(assets_url_path)),
                                            href='https://github.com/Grasia/WikiChron',
                                            target='_blank',
                                            className='icon',
                                            title='Github repo'
                                        ),
                                    ],
                                    id='icons-bar')
                                ]
                            )
                        ]
                    )
                ]
            )
        );


    def share_modal(share_link, download_link):
        return html.Div([
            sd_material_ui.Dialog(
                html.Div(children=[
                    html.H3('Share WikiChron with others or save your work!'),
                    html.P([
                      html.Strong('Link with your current selection:'),
                      html.Div(className='share-modal-link-and-button-cn', children=[
                        dcc.Input(value=share_link, id='share-link-input', readOnly=True, className='share-modal-input-cn', type='url'),
                        html.Div(className='tooltip', children=[
                          html.Button('Copy!', id='share-link', className='share-modal-button-cn'),
                        ])
                      ]),
                    ]),
                    html.P([
                      html.Strong('Link to download the data of your current selection:'),
                      html.Div(className='share-modal-link-and-button-cn', children=[
                        dcc.Input(value=download_link, id='share-download-input', readOnly=True, className='share-modal-input-cn', type='url'),
                        html.Div(className='tooltip', children=[
                          html.Button('Copy!', id='share-download', className='share-modal-button-cn'),
                        ])
                      ]),

                      html.Div([
                        html.Span('You can find more info about working with the data downloaded in '),
                        html.A('this page of our wiki.', href='https://github.com/Grasia/WikiChron/wiki/Downloading-and-working-with-the-data')
                        ],
                        className='share-modal-paragraph-info-cn'
                      )
                    ]),
                    gdc.Import(src='/js/common/dash/main.share_modal.js')
                    ],
                    id='share-dialog-inner-div'
                ),
                id='share-dialog',
                modal=False,
                open=False
            )
        ])


    def select_wikis_and_metrics_control(wikis_dropdown_options, metrics_dropdown_options):
        return html.Div(
                    id='wikis-and-metrics-control',
                    className='selector',
                    children=[
                        html.Div(id='first-row',
                            className='row',
                            children=[
                                html.Span(
                                'You are comparing:',
                                className='two columns comparing-label'
                                ),

                                html.Div(id='wikis-selection-div',
                                    children=[
                                        html.Strong('Wikis:',
                                            className='one column dropdown-label',
                                        ),

                                        dcc.Dropdown(
                                            id='wikis-selection-dropdown',
                                            className='four columns wikis-selection-dropdown-cls',
                                            options=wikis_dropdown_options,
                                            multi=True,
                                            searchable=False,
                                            value=[ option['value'] for option in wikis_dropdown_options ]
                                        ),
                                    ]
                                ),

                                html.Div(id='metrics-selection-div',
                                    children=[
                                        html.Strong('Metrics:',
                                            className='one column dropdown-label',
                                        ),

                                        dcc.Dropdown(
                                            id='metrics-selection-dropdown',
                                            className='four columns',
                                            options=metrics_dropdown_options,
                                            multi=True,
                                            searchable=False,
                                            value=[ option['value'] for option in metrics_dropdown_options ]
                                        ),
                                    ]
                                )
                            ],
                        )
                    ]
                );


    def select_time_axis_control(init_relative_time):
        return (html.Div(
                id='time-axis-selection-div',
                className='selector row',
                children=[
                    html.Span(
                        'Time axis:',
                        className='two columns'
                    ),
                    dcc.RadioItems(
                        options=[
                            {'label': 'Months from birth', 'value': 'relative'},
                            {'label': 'Calendar dates', 'value': 'absolute'}
                        ],
                        value=init_relative_time,
                        id='time-axis-selection',
                        labelClassName='time-axis-label',
                        inputClassName='time-axis-input',
                        style={'display': 'inline-flex'}
                    ),
                ],
                style={'margin-top' : '15px'}
            )
        );


    def date_slider_control():
        return (html.Div(id='date-slider-div',
                className='row selector',
                children=[
                    html.Span('Time interval (months):',
                        className='two columns'
                    ),
                    html.Div(id='date-slider-container',
                        className='nine columns',
                        style={'height': '35px', 'margin-left': 0},
                        children=[
                            dcc.RangeSlider(
                                id='dates-slider',
                        )],
                    ),
                    html.Div(className='one column')
                ],
                )
        );


    wikis = wikis_arg;
    metrics = metrics_arg;
    relative_time = relative_time_arg;

    if debug:
        print ('Generating main...')

    wikis_dropdown_options = []
    for index, wiki in enumerate(wikis):
        wikis_dropdown_options.append({'label': wiki['name'], 'value': index})

    metrics_dropdown_options = []
    for index, metric in enumerate(metrics):
        metrics_dropdown_options.append({'label': metric.text, 'value': index})

    metrics_code = [metric.code for metric in metrics]
    args_selection = json.dumps({"wikis": wikis, "metrics": metrics_code, "relative_time": relative_time})

    share_url_path = f'{server_config["PREFERRED_URL_SCHEME"]}://{server_config["APP_HOSTNAME"]}{mode_config["DASH_BASE_PATHNAME"]}{query_string}'
    download_url_path = f'{server_config["PREFERRED_URL_SCHEME"]}://{server_config["APP_HOSTNAME"]}{mode_config["DASH_DOWNLOAD_PATHNAME"]}{query_string}'

    selection_url = f'{mode_config["HOME_MODE_PATHNAME"]}selection/{query_string}'

    return html.Div(id='main',
        className='control-text',
        children=[

            main_header(),

            html.Div(id='selection-div',
                className='container',
                children=[
                    select_wikis_and_metrics_control(wikis_dropdown_options, metrics_dropdown_options),
                    select_time_axis_control('relative' if relative_time else 'absolute'),
                    date_slider_control(),
                ]
             ),

            html.Div(id='graphs'),

            share_modal(share_url_path, download_url_path),

            html.Div(id='initial-selection', style={'display': 'none'}, children=args_selection),
            html.Div(id='signal-data', style={'display': 'none'}),
            html.Div(id='time-axis', className='time-index', style={'display': 'none'}),
            html.Div(id='ready', style={'display': 'none'}),
            gdc.Import(src='/js/common/dash/sliderHandlerLabels.js')
        ]
    );

def bind_callbacks(app):

    @app.callback(
        Output('signal-data', 'children'),
        [Input('initial-selection', 'children')]
    )
    def start_main(selection_json):
        # get wikis x metrics selection
        selection = json.loads(selection_json)
        wikis = selection['wikis']
        metrics = extract_metrics_objs_from_metrics_codes(selection['metrics'])

        metric_names = [metric.text for metric in metrics]
        wikis_names = [wiki['name'] for wiki in wikis]
        print('--> Retrieving and computing data')
        print( '\t for the following wikis: {}'.format( wikis_names ))
        print( '\tof the following metrics: {}'.format( metric_names ))
        data = data_controller.load_and_compute_data(wikis, metrics)
        print('<-- Done retrieving and computing data!')
        return True


    @app.callback(
        Output('time-axis', 'children'),
        [Input('signal-data', 'children'),
        Input('time-axis-selection', 'value'),
        ],
        [State('initial-selection', 'children'),]
    )
    def time_axis(signal, selected_timeaxis, selection_json):
        if not signal or not selected_timeaxis or not selection_json:
            return '';

        relative_time = selected_timeaxis == 'relative'

        # get wikis x metrics selection
        selection = json.loads(selection_json)
        wikis = selection['wikis']
        metrics = extract_metrics_objs_from_metrics_codes(selection['metrics'])

        data = data_controller.load_and_compute_data(wikis, metrics)

        # get time axis of the oldest one and use it as base numbers for the slider:
        time_axis_index = data_controller.generate_longest_time_axis([ wiki for wiki in data[0] ],
                                                    relative_time)

        if relative_time:
            return json.dumps(time_axis_index)
        else:
            return json.dumps(time_axis_index.date.tolist(), default=str)


    @app.callback(
        Output('ready', 'children'),
        [Input('wikis-selection-dropdown', 'value'),
        Input('metrics-selection-dropdown', 'value'),
        Input('dates-slider', 'value'),
        Input('time-axis-selection', 'value'),
        Input('signal-data', 'children'),
        Input('time-axis', 'children')],
    )
    def ready_to_plot_graphs(*args):
        #~ print (args)
        if not all(args):
            #~ print('not ready!')
            return None
        else:
            if debug:
                print('Ready to plot graphs!')
            return 'ready'


    @app.callback(
        Output('graphs', 'children'),
        [Input('ready', 'children')],
        [State('wikis-selection-dropdown', 'value'),
        State('metrics-selection-dropdown', 'value'),
        State('dates-slider', 'value'),
        State('time-axis-selection', 'value'),
        State('initial-selection', 'children'),
        State('time-axis', 'children')]
    )
    def update_graphs(ready,
            selected_wikis, selected_metrics, selected_timerange,
            selected_timeaxis, selection_json, time_axis_json):

        if not ready: # waiting for all parameters to be ready
            return;

        # get wikis x metrics selection
        selection = json.loads(selection_json)
        wikis = selection['wikis']
        metrics = extract_metrics_objs_from_metrics_codes(selection['metrics'])

        data = data_controller.load_and_compute_data(wikis, metrics)

        if debug:
            print('Updating graphs. Selection: [{}, {}, {}, {}]'.format(selected_wikis, selected_metrics, selected_timerange, selected_timeaxis))

        relative_time = selected_timeaxis == 'relative'

        time_start_generating_graphs = time.perf_counter()
        new_graphs = generate_graphs(data, metrics, wikis, relative_time);
        time_end_generating_graphs = time.perf_counter() - time_start_generating_graphs
        print(' * [Timing] Generating graphs : {} seconds'.format(time_end_generating_graphs) )

        from sys import getsizeof
        print('Size of graphs in memory: {} bytes.'.format(getsizeof(new_graphs)))

        for i, metric in enumerate(metrics):
            for j, wiki in enumerate(wikis):
                metric_data = new_graphs[i][j]
                if relative_time:
                    x_axis = list(range(len(metric_data.x))) # relative to the age of the wiki in months
                else:
                    x_axis = metric_data.x # natural months
            new_graphs[i][j].x = x_axis

        for wiki_idx in range(len(wikis)):
            if wiki_idx in selected_wikis:
                for metric_idx in range(len(metrics)):
                    new_graphs[metric_idx][wiki_idx]['visible'] = True
            else:
                for metric_idx in range(len(metrics)):
                    new_graphs[metric_idx][wiki_idx]['visible'] = "legendonly"


        # Show only the selected timerange in the slider.
        new_timerange = selected_timerange

        # In case we are displaying calendar dates, then we have to do a
        # conversion from "relative dates" to the actual 'natural' date.
        if not relative_time:
            time_axis = pd.DatetimeIndex(json.loads(time_axis_json))
            new_timerange[0] = time_axis[selected_timerange[0]]
            new_timerange[1] = time_axis[selected_timerange[1]]

        # Dash' graphs:
        dash_graphs = []
        for i, metric in enumerate(metrics):
            if (i in selected_metrics):
                dash_graphs.append(
                    dcc.Graph(
                        id='graph-{}'.format(i),
                        figure={
                            'data': new_graphs[i],
                            'layout': {
                                'title': metric.text,
                                'xaxis': {'range': new_timerange }
                            }
                        },
                        config={
                            'displaylogo': False,
                            'showLink': False,
                            'modeBarButtonsToRemove': ['sendDataToCloud']
                        }
                    )
                )

        return dash_graphs # update_graphs


    @app.callback(
        Output('date-slider-container', 'children'),
        [Input('time-axis', 'children'),
        Input('time-axis-selection', 'value')],
        [State('dates-slider', 'value')]
    )
    def update_slider(time_axis_json, selected_timeaxis, slider_previous_state):
        """
        data -- to extract the selected wikis (to obtain the time axis index)
        time_axis_selection -- To know if we're in relative or calendar dates
        Returns a dcc.RangeSlider in dates-slider
        """

        if not time_axis_json:
            return dcc.RangeSlider(id='dates-slider');

        relative_time = selected_timeaxis == 'relative'

        time_axis = json.loads(time_axis_json)

        # If using calendar dates, work with pandas DatetimeIndex
        # (equivalent to Python datetime), so we can use strftime()
        if not relative_time:
            time_axis = pd.DatetimeIndex(time_axis)

        min_time = 0
        max_time = len (time_axis)

        #~ max_number_of_marks = 11
        if max_time < 12:
            step_for_marks = 1
        elif max_time < 33:
            step_for_marks = 3
        elif max_time < 66:
            step_for_marks = 6
        elif max_time < 121:
            step_for_marks = 12
        elif max_time < 264:
            step_for_marks = 24
        else:
            step_for_marks = 36

        # Take dates starting from month 0 in steps defined by step_for_marks
        #  (which makes sure that you don't have more than 11 points in the slider)
        #  and skip (don't take) the last mark since we want to put there the last
        #  month of the wiki.
        subset_times = time_axis[0:max_time-step_for_marks:step_for_marks]

        if relative_time:
            range_slider_marks = {x: str(x) for x in subset_times}
            range_slider_marks[max_time-1] = max_time-1
        else:
            range_slider_marks = {i*step_for_marks: x.strftime('%b %Y') for i, x in enumerate(subset_times)}
            range_slider_marks[max_time-1] = time_axis[max_time-1].strftime('%b %Y')

        if slider_previous_state:
            value = slider_previous_state
        else:
            value = [min_time, max_time-1]

        return (
                    dcc.RangeSlider(
                        id='dates-slider',
                        min=min_time,
                        max=max_time-1,
                        step=1,
                        value=value,
                        allowCross=False,
                        marks=range_slider_marks,
                    )
                )


    @app.callback(
        Output('share-dialog', 'open'),
        [Input('share-button', 'n_clicks')],
        [State('share-dialog', 'open')]
    )
    def show_share_modal(n_clicks: int, open_state: bool):
        if not n_clicks: # modal init closed
            return False
        elif n_clicks > 0 and not open_state: # opens if we click and `open` state is not open
            return True
        else: # otherwise, leave it closed.
            return False


    # Play with this in case we want to download only the being shown current selection
    # instead of the generate_main_content() selection
    #@app.callback(
        #Output('download-button', 'href'),
        #[Input('current-selection-wikis', 'children')], -> Coming from Dropdowns
        #[Input('current-selection-metrics', 'children')], -> Coming from Dropdowns
    #)
    #def set_href_for_download_button(selection_json):
        #selection = json.loads(selection_json)
        #print(selection)
        #query_str = urlencode(selection,  doseq=True)
        #href = '/download/?' + query_str;
        #return href

    return # bind_callbacks
