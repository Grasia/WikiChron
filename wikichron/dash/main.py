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
import functools
from urllib.parse import urlencode

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output, State
import grasia_dash_components as gdc
import sd_material_ui

# Local imports:
import lib.interface as lib
from cache import cache

global debug
debug = True if os.environ.get('FLASK_ENV') == 'development' else False


def extract_metrics_objs_from_metrics_codes(metric_codes):
    metrics = [ lib.metrics_dict[metric] for metric in metric_codes ]
    return metrics


@cache.memoize(timeout=3600)
def load_data(wiki):
    df = lib.get_dataframe_from_csv(wiki['data'])
    lib.prepare_data(df)
    df = clean_up_bot_activity(df, wiki)
    return df


def clean_up_bot_activity(df, wiki):
    if 'botsids' in wiki:
        return lib.remove_bots_activity(df, wiki['botsids'])
    else:
        warn("Warning: Missing information of bots ids. Note that graphs can be polluted of non-human activity.")
        return df


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


# returns data[metric][wiki]
@cache.memoize()
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

@cache.memoize()
def generate_longest_time_axis(list_of_selected_wikis, relative_time):
    """ Generate time axis index of the oldest wiki """

    # Make the union of the Datetime indices of every wiki.
    # In this way, we get the date range corresponding of the smallest set that
    #  covers all the lifespan of all wikis.
    # Otherwise, wikis lifespan for different dates which are not
    #  contained in the lifespan of the oldest wiki would be lost
    unified_datetime_index = functools.reduce(
                            lambda index_1, index_2: index_1.union(index_2),
                            map(lambda wiki: wiki.index, list_of_selected_wikis))
    if relative_time:
        time_axis = list(range(0, len(unified_datetime_index)))
    else:
        time_axis = unified_datetime_index
    return time_axis


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
                            query_string, url_host):

    def main_header():
        href_download_button = '/download/{}'.format(query_string)
        return (html.Div(id='header',
                className='container',
                style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between'},
                children=[
                    html.Span(
                        html.Img(src='/assets/logo_wikichron.svg'),
                        id='tool-title'),
                    html.Div([
                        html.A(
                            html.Img(src='/assets/share.svg'),
                            id='share-button',
                            className='icon',
                            title='Share current selection'
                        ),
                        html.A(
                            html.Img(src='/assets/cloud_download.svg'),
                            href=href_download_button,
                            id='download-button',
                            target='_blank',
                            className='icon',
                            title='Download data'
                        ),
                        html.A(
                            html.Img(src='/assets/documentation.svg'),
                            href='https://github.com/Grasia/WikiChron/wiki/',
                            target='_blank',
                            className='icon',
                            title='Documentation'
                        ),
                        html.A(
                            html.Img(src='/assets/ico-github.svg'),
                            href='https://github.com/Grasia/WikiChron',
                            target='_blank',
                            className='icon',
                            title='Github repo'
                        ),
                    ],
                    id='icons-bar')
            ])
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
                    gdc.Import(src='js/main.share_modal.js')
                    ],
                    id='share-dialog-inner-div'
                ),
                id='share-dialog',
                modal=False,
                open=False
            )
        ])


    def select_wikis_and_metrics_control(wikis_dropdown_options, metrics_dropdown_options):
        return (html.Div(id='wikis-and-metrics-control',
                        className='selector',
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
                                ]
                            ),

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
                            ],
                        )
                );

    def select_time_axis_control(init_relative_time):
        return (html.Div([
            html.Div([
                html.Span(
                    [html.Strong('Time axis:')],
                    className='three columns',
                    style={'padding-left': '7.5%'}
                ),
                dcc.RadioItems(
                    options=[
                        {'label': 'Months from birth', 'value': 'relative'},
                        {'label': 'Calendar dates', 'value': 'absolute'}
                    ],
                    value=init_relative_time,
                    id='time-axis-selection',
                    inputStyle={'margin-left': '0px'}
                ),
                ],
                id='time-axis-selection-div',
                className='selector'
            ),
            ],
            style={'margin-top' : '15px'}
            )
        );


    def date_slider_control():
        return (html.Div(id='date-slider-div', className='container',
                children=[
                    html.Span(id='slider-header',
                    children=[
                        html.Strong(
                            'Time interval (months):'),
                        html.Span(id='display-slider-selection')
                    ]),

                    html.Div(id='date-slider-container',
                        style={'height': '35px'},
                        children=[
                            dcc.RangeSlider(
                                id='dates-slider',
                        )],
                    )
                ],
                style={'margin-top': '15px'}
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

    return html.Div(id='main',
        className='control-text',
        style={'width': '100%'},
        children=[

            main_header(),

            html.Hr(),

            html.Div(id='selection-div',
                className='container',
                children=[
                    select_wikis_and_metrics_control(wikis_dropdown_options, metrics_dropdown_options),
                    select_time_axis_control('relative' if relative_time else 'absolute')
                ]
             ),

            date_slider_control(),

            html.Hr(),

            html.Div(id='graphs'),

            share_modal('{}/app/{}'.format(url_host, query_string),
                        '{}/download/{}'.format(url_host, query_string)),

            html.Div(id='initial-selection', style={'display': 'none'}, children=args_selection),
            html.Div(id='signal-data', style={'display': 'none'}),
            html.Div(id='time-axis', style={'display': 'none'}),
            html.Div(id='ready', style={'display': 'none'})
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
        data = load_and_compute_data(wikis, metrics)
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

        data = load_and_compute_data(wikis, metrics)

        # get time axis of the oldest one and use it as base numbers for the slider:
        time_axis_index = generate_longest_time_axis([ wiki for wiki in data[0] ],
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

        data = load_and_compute_data(wikis, metrics)

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
        Output('display-slider-selection', 'children'),
        [Input('dates-slider', 'value')],
        [State('time-axis-selection', 'value'),
        State('time-axis', 'children')]
    )
    def display_slider_selection(slider_selection, selected_timeaxis, time_axis_json):
        """
        Shows the selected time range from the slider in a text block.
        slider_selection -- Selection of the Range Slider.
        """

        if not slider_selection or not time_axis_json:
            return;

        relative_time = selected_timeaxis == 'relative'

        if relative_time:
            return('From month {} to month {} after the birthdate of the oldest wiki.'.
                format(slider_selection[0], slider_selection[1]))

        # In case we are displaying calendar dates, then we have to do a
        # conversion from "relative dates" to the actual 'natural' date.
        else:
            new_timerange = [0,0]
            time_axis = pd.DatetimeIndex(json.loads(time_axis_json))
            new_timerange[0] = time_axis[slider_selection[0]].strftime('%b %Y')
            new_timerange[1] = time_axis[slider_selection[1]].strftime('%b %Y')
            return('From {} to {} '.format(new_timerange[0], new_timerange[1]))


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
