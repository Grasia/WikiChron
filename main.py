#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   main.py

   Descp: Generate the main content of the webapp:
Title, plots and filter elements.

   Created on: 01-nov-2017

   Copyright 2017 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

import os
import time
from warnings import warn
import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output, State

# Local imports:
import lib.interface as lib
from cache import cache

global debug
debug = 'DEBUG' in os.environ

# get csv data location (data/ by default)
global data_dir;
data_dir = os.getenv('WIKICHRON_DATA_DIR', 'data')

#~ wikis_df = []
#~ global wikis, metrics
#~ wikis = []
#~ metrics = []

#~ graphs = []

#~ global min_time, max_time; # global variables to store the max and min values for the time axis. -> Slider

#~ global relative_time; # flag to know when we're plotting in relative dates
#~ global times_axis; # datetime index of the oldest wiki from the selected subset of wikis.


@cache.memoize(timeout=3600)
def load_data(wiki):
    df = get_dataframe_from_csv(wiki['data'])
    lib.prepare_data(df)
    df = clean_up_bot_activity(df, wiki)
    return df


def get_dataframe_from_csv(csv):
    """ Read and parse a csv and return the corresponding pandas dataframe"""
    print('Loading csv for ' + csv)
    time_start_loading_one_csv = time.perf_counter()
    df = pd.read_csv(os.path.join(data_dir, csv),
                    delimiter=';', quotechar='|',
                    index_col=False)
    df['timestamp']=pd.to_datetime(df['timestamp'],format='%Y-%m-%dT%H:%M:%SZ')
    #~ df.set_index(df['timestamp'], inplace=True) # generate a datetime index
    #~ print(df.info())
    print('!!Loaded csv for ' + csv)
    time_end_loading_one_csv = time.perf_counter() - time_start_loading_one_csv
    print(' * [Timing] Loading {} : {} seconds'.format(csv, time_end_loading_one_csv) )

    return df


def clean_up_bot_activity(df, wiki):
    if 'botsids' in wiki:
        return lib.remove_bots_activity(df, wiki['botsids'])
    else:
        warn("Warning: Missing information of bots ids. Note that graphs can be polluted of non-human activity.")
        return df


@cache.memoize()
def compute_data(dataframes, metrics):
    """ Load analyzed data by every metric for every dataframe and store it in data[] """

    #~ if not relative_time: # natural time index
        #~ return [ lib.compute_metric_on_dataframes(metric, dataframes) for metric in metrics]
    #~ else: # relative time index
    metrics_by_wiki = []
    for df in dataframes:
        metrics_by_wiki.append(lib.compute_metrics_on_dataframe(metrics, df))

    # transposing matrix row=>wikis, column=>metrics to row=>metrics, column=>wikis
    wiki_by_metrics = []
    for metric_idx in range(len(metrics)):
        metric_row = [metrics_by_wiki[wiki_idx].pop(0) for wiki_idx in range(len(metrics_by_wiki))]
        wiki_by_metrics.append(metric_row)

    return wiki_by_metrics


def load_and_compute_data(wikis, metrics):

    # load data from csvs:
    time_start_loading_csvs = time.perf_counter()
    wikis_df = []
    for wiki in wikis:
        df = load_data(wiki)
        wikis_df.append(df)
    time_end_loading_csvs = time.perf_counter() - time_start_loading_csvs
    print(' * [Timing] Loading csvs : {} seconds'.format(time_end_loading_csvs) )

    # compute metric data:
    print(' * [Info] Starting calculations....')
    time_start_calculations = time.perf_counter()
    data = compute_data(wikis_df, metrics)
    time_end_calculations = time.perf_counter() - time_start_calculations
    print(' * [Timing] Calculations : {} seconds'.format(time_end_calculations) )
    return data


def generate_graphs(data, metrics, wikis, relative_time):
    """ Turn over data[] into plotly graphs objects and store it in graphs[] """

    #~ global min_time, max_time, times_axis;

    graphs_list = [[None for j in range(len(wikis))] for i in range(len(metrics))]

    #~ global metric_data
    for metric_idx in range(len(metrics)):
        for wiki_idx in range(len(wikis)):
            metric_data = data[metric_idx][wiki_idx]
            if relative_time:
                x_axis = len(metric_data.index) # relative to the age of the wiki in months
            else:
                x_axis = metric_data.index # natural months

            graphs_list[metric_idx][wiki_idx] = go.Scatter(
                                x=x_axis,
                                y=metric_data.data,
                                name=wikis[wiki_idx]['name']
                                )

    # The oldest wiki is the one with longer number of months
    oldest_wiki = max(data[0],key = lambda wiki: len(wiki))
    min_time = 0
    max_time = len (oldest_wiki)
    if relative_time:
        times_axis = list(range(min_time, max_time))
    else:
        times_axis = oldest_wiki.index

    return graphs_list


def select_time_axis_control(init_relative_time):
    return (html.Div([
        html.Div([
            html.Strong('Time axis:'),
            dcc.RadioItems(
                options=[
                    {'label': 'Months from birth', 'value': 'relative'},
                    {'label': 'Calendar dates', 'value': 'absolute'}
                ],
                value=init_relative_time,
                id='time-axis-selection'
            ),
            ],
            className="container"
        ),
        ])
    )


def generate_main_content(wikis_arg, metrics_arg, relative_time_arg):
    #~ global wikis_df, data, graphs, wikis, metrics, min_time, max_time, relative_time;

    wikis = wikis_arg;
    metrics = metrics_arg;
    relative_time = relative_time_arg;

    print ('Generating main...')

    wikis_dropdown_options = []
    for index, wiki in enumerate(wikis):
        wikis_dropdown_options.append({'label': wiki['name'], 'value': index})

    metrics_dropdown_options = []
    for index, metric in enumerate(metrics):
        metrics_dropdown_options.append({'label': metric.text, 'value': index})

    metrics_code = [metric.code for metric in metrics]
    args_selection = json.dumps({"wikis": wikis, "metrics": metrics_code, "relative_time": relative_time})

    return html.Div(id='main',
        className='control-text',
        style={'width': '100%'},
        children=[

            html.Div(id='header',
                className='container',
                style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between'},
                children=[
                    html.Span(
                        html.Img(src='assets/logo_wikichron.svg'),
                        id='tool-title'),
                    html.Div([
                        html.A(
                            html.Img(src='assets/documentation.svg'),
                            href='https://github.com/Grasia/WikiChron/wiki/',
                            target='_blank',
                            className='icon',
                            title='Documentation'
                        ),
                        html.A(
                            html.Img(src='assets/ico-github.svg'),
                            href='https://github.com/Grasia/WikiChron',
                            target='_blank',
                            className='icon',
                            title='Github repo'
                        ),
                    ],
                    id='icons-bar')
            ]),
            html.Hr(),

            html.Div(id='selection-div',
                className='container',
                children=[
                    html.Div(id='first-row',
                        className='row',
                        style={'marginBottom': '15px'},
                        children=[
                            html.Strong(
                            'You are comparing:',
                            className='three columns'
                            ),

                    html.Div(id='wikis-selection-div',
                        children=[
                            html.Span('Wikis:', className='two columns'),

                            dcc.Dropdown(
                                id='wikis-selection-dropdown',
                                className='seven columns',
                                options=wikis_dropdown_options,
                                multi=True,
                                searchable=False,
                                value=[ option['value'] for option in wikis_dropdown_options ]
                             ),
                         ]),
                    ]),

                html.Div(id='metrics-selection-div',
                        className='row',
                        children=[
                            html.P(className='three columns'),
                            html.Span('Metrics:', className='two columns', style={'marginLeft': '0'}),

                            dcc.Dropdown(
                                id='metrics-selection-dropdown',
                                className='seven columns',
                                options=metrics_dropdown_options,
                                multi=True,
                                searchable=False,
                                value=[ option['value'] for option in metrics_dropdown_options ]
                            ),
                         ]),

                select_time_axis_control('relative' if relative_time else 'absolute')

             ]),

            html.Hr(),

            html.Div(id='date-slider-div', className='container'),

            html.Div(id='graphs'),

            html.Div(id='initial-selection', style={'display': 'none'}, children=args_selection),
            html.Div(id='intermediate-data', style={'display': 'none'})
        ]
    );

def bind_callbacks(app):

    @app.callback(
        Output('intermediate-data', 'children'),
        [Input('initial-selection', 'children')]
        )
    def start_main(selection_json):
        selection = json.loads(selection_json)
        wikis = selection['wikis']
        metrics = [ lib.metrics_dict[metric] for metric in selection['metrics'] ]

        metric_names = [metric.text for metric in metrics]
        wikis_names = [wiki['name'] for wiki in wikis]
        print('--> Retrieving and computing data')
        print( '\t for the following wikis: {}'.format( wikis_names ))
        print( '\tof the following metrics: {}'.format( metric_names ))
        data = load_and_compute_data(wikis, metrics)
        print('<-- Done retrieving and computing data!')
        return json.dumps(data, default=lambda ts: ts.to_json(force_ascii=False))


    @app.callback(
        Output('graphs', 'children'),
        [Input('wikis-selection-dropdown', 'value'),
        Input('metrics-selection-dropdown', 'value'),
        Input('time-axis-selection', 'value'),
        Input('intermediate-data', 'children')],
        [State('initial-selection', 'children')]
    )
    def update_graphs(selected_wikis, selected_metrics, #selected_timerange,
            selected_timeaxis, data_json, selection_json):

        if not data_json: # waiting for data to be retrieved and calculated from server
            return;

        selection = json.loads(selection_json)
        wikis = selection['wikis']
        metrics = [ lib.metrics_dict[metric] for metric in selection['metrics'] ]

        data = json.loads(data_json)
        for i in range(len(data)):
            for j in range(len(data[i])):
                data[i][j] = pd.read_json(data[i][j], typ="series")

        #~ print('Updating graphs. Selection: [{}, {}, {}, {}]'.format(selected_wikis, selected_metrics, selected_timerange, selected_timeaxis))
        print('Updating graphs. Selection: [{}, {}, {}]'.format(selected_wikis, selected_metrics, selected_timeaxis))

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
                    x_axis = len(metric_data.y) # relative to the age of the wiki in months
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


        # Showing only the selected timerange in the slider.
        #~ new_timerange = selected_timerange
        # In case we are displaying calendar dates, then we have to do a conversion:
        #~ if not relative_time:
            #~ new_timerange[0] = times_axis[selected_timerange[0]]
            #~ new_timerange[1] = times_axis[selected_timerange[1]]

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
                                #~ 'xaxis': {'range': new_timerange }
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

    """
    @app.callback(
        Output('graphs', 'children'),
        [Input('wikis-selection-dropdown', 'value'),
        Input('metrics-selection-dropdown', 'value'),
        Input('dates-slider', 'value'),
        Input('time-axis-selection', 'value')],
        [State('intermediate-data', 'children')]
    )
    # input -> min_time, max_time, time_axis
    # output -> dates-slider
    # IMPORTANT!! -> Make sure output does not activate update_graphs, but both update_slider and update_graphs are activated at same time.
    def update_slider():

        number_of_marks = int(len(times_axis) / 9);
        subset_times = times_axis[0::number_of_marks]
        #~ last_element = times_axis[max_time-1]
        if relative_time:
            range_slider_marks = {x: str(x) for x in subset_times}
            #~ range_slider_marks[max_time] = str(last_element)
        else:
            range_slider_marks = {i*number_of_marks: x.strftime('%b %Y') for i, x in enumerate(subset_times)}
            #~ range_slider_marks[max_time] = last_element.strftime('%b %Y')

        # parts of this should be on main actually:
        return children=[

                        html.Strong(
                            'Time interval (months)'),

                        html.Div(
                            dcc.RangeSlider(
                                id='dates-slider',
                                min=min_time,
                                max=max_time-1,
                                step=1,
                                value=[min_time, max_time-1],
                                allowCross=False,
                                marks=range_slider_marks,
                            ),
                            style={'height': '35px'}
                        )
                   ]),

    """

    return # bind_callbacks

if __name__ == '__main__':

    data_dir = os.getenv('WIKICHRON_DATA_DIR', 'data')

    wikis = ['eslagunanegra_pages_full', 'cocktails', 'es.shamanking.wikia.com']

    available_metrics = lib.get_available_metrics()
    metrics = []
    metrics.append(available_metrics[0])
    metrics.append(available_metrics[1])

    app = dash.Dash()
    app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
    app.css.append_css({"external_url": "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css"})

    relative_time = False
    app.layout = generate_main_content(wikis, metrics, relative_time)

    bind_callbacks(app)

    app.run_server(debug=debug, port=8053)
