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

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output

# Local imports:
import lib.interface as lib

global debug
debug = 'DEBUG' in os.environ

# get csv data location (data/ by default)
global data_dir;
data_dir = os.getenv('WIKICHRON_DATA_DIR', 'data')

wikis_df = []
global wikis, metrics
wikis = []
metrics = []

data = [] # matrix of panda series, being rows => metric and columns => wiki
graphs = []

global min_time, max_time; # global variables to store the max and min values for the time axis.

global relative_time; # flag to know when we're plotting in relative dates
global times_axis; # datetime index of the oldest wiki from the selected subset of wikis.

def get_dataframe_from_csv(csv):
    """ Read and parse a csv and return the corresponding pandas dataframe"""
    print('Loading csv for ' + csv)
    df = pd.read_csv(os.path.join(data_dir, csv + '.csv'),
                    delimiter=';', quotechar='|',
                    index_col='revision_id')
    df['timestamp']=pd.to_datetime(df['timestamp'],format='%Y-%m-%dT%H:%M:%SZ')
    #~ df.set_index(df['timestamp'], inplace=True) # generate a datetime index
    #~ print(df.info())
    print('!!Loaded csv for ' + csv)
    return df


def load_data(dataframes, metrics):
#~ def load_data(dataframes, metrics, relative_time):
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

def generate_graphs(metrics, wikis, relative_time):
    """ Turn over data[] into plotly graphs objects and store it in graphs[] """

    global min_time, max_time, times_axis;

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
                                name=wikis[wiki_idx]
                                )

    oldest_wiki = max(data[0],key = lambda wiki: len(wiki))
    min_time = 0
    max_time = len (oldest_wiki)
    if relative_time:
        times_axis = list(range(min_time, max_time))
    else:
        times_axis = oldest_wiki.index

    return graphs_list


def generate_main_content(wikis_arg, metrics_arg, relative_time_arg):
    global wikis_df, data, graphs, wikis, metrics, min_time, max_time, relative_time;
    wikis = wikis_arg;
    metrics = metrics_arg;
    relative_time = relative_time_arg;

    wikis_df = [get_dataframe_from_csv(wiki) for wiki in wikis]

    data = load_data(wikis_df, metrics)
    graphs = generate_graphs(metrics, wikis, relative_time)

    wikis_dropdown_options = []
    for index, wiki in enumerate(wikis):
        wikis_dropdown_options.append({'label': wiki, 'value': index})

    metrics_dropdown_options = []
    for index, metric in enumerate(metrics):
        metrics_dropdown_options.append({'label': metric.text, 'value': index})

    number_of_marks = int(len(times_axis) / 9);
    subset_times = times_axis[0::number_of_marks]
    #~ last_element = times_axis[max_time-1]
    if relative_time:
        range_slider_marks = {x: str(x) for x in subset_times}
        #~ range_slider_marks[max_time] = str(last_element)
    else:
        range_slider_marks = {i*number_of_marks: x.strftime('%b %Y') for i, x in enumerate(subset_times)}
        #~ range_slider_marks[max_time] = last_element.strftime('%b %Y')

    return html.Div(id='main',
        style={'width': '100%'},
        children=[

            html.Div(id='header',
                className='container',
                style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between'},
                children=[
                    html.H1('WIKI CHRON', id='tool-title'),
                    html.A(
                        html.Img(src='assets/ico-github.svg'),
                        href='https://github.com/Grasia/WikiChron',
                        style={'margin-left': 'auto'},
                        target='_blank'
                    ),
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
                            html.Strong('Wikis:', className='two columns'),

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
                            html.Strong('Metrics:', className='two columns', style={'marginLeft': '0'}),

                            dcc.Dropdown(
                                id='metrics-selection-dropdown',
                                className='seven columns',
                                options=metrics_dropdown_options,
                                multi=True,
                                searchable=False,
                                value=[ option['value'] for option in metrics_dropdown_options ]
                            ),
                         ])
             ]),

            html.Hr(),

            html.Div(id='date-slider-div',
                    className='container',
                    children=[

                        html.Strong(
                            'Select your temporary range:'),

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

            html.Div(id='graphs')
        ]
    );

def bind_callbacks(app):
    @app.callback(
        Output('graphs', 'children'),
        [Input('wikis-selection-dropdown', 'value'),
        Input('metrics-selection-dropdown', 'value'),
        Input('dates-slider', 'value')])
    def update_graphs(selected_wikis, selected_metrics, selected_timerange):
        global relative_time;

        for wiki_idx in range(len(wikis)):
            if wiki_idx in selected_wikis:
                for metric_idx in range(len(metrics)):
                    graphs[metric_idx][wiki_idx]['visible'] = True
            else:
                for metric_idx in range(len(metrics)):
                    graphs[metric_idx][wiki_idx]['visible'] = "legendonly"

        dash_graphs = []

        if not relative_time:
            selected_timerange[0] = times_axis[selected_timerange[0]]
            selected_timerange[1] = times_axis[selected_timerange[1]]

        for i, metric in enumerate(metrics):
            if (i in selected_metrics):
                dash_graphs.append(
                    dcc.Graph(
                    id='graph-{}'.format(i),
                    figure={
                        'data': graphs[i],
                        'layout': {
                            'title': metric.text,
                            'xaxis': {'range': selected_timerange }
                        }
                    }
                    )
                )

        return html.Div(
            id='graphs',
            children=dash_graphs
        )

    return

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
