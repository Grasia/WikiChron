#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   main.py

   Descp: Generate the main content of the webapp:
Title, plots and filter elements.

   Created on: 01-nov-2017

   Copyright 2017 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output

wikis = ['eslagunanegra_pages_full', 'cocktails', 'zelda']
wikis_df = []

metrics = ['edits_monthly', 'users_new']

data_edits_pages_monthly = []
data_new_users_monthly = []
data = [data_edits_pages_monthly, data_new_users_monthly]


def get_data_from_csv(csv):
    print('Loading csv for ' + csv)
    df = pd.read_csv('data/' + csv + '.csv',
                    delimiter=';', quotechar='|',
                    index_col='revision_id')
    df['timestamp']=pd.to_datetime(df['timestamp'],format='%Y-%m-%dT%H:%M:%SZ')
    #~ df.set_index(df['timestamp'], inplace=True) # generate a datetime index
    #~ print(df.info())
    print('!!Loaded csv for ' + csv)
    return df


def generate_graphs():

    for i, data in enumerate(wikis_df):
        monthly_data = data.groupby(pd.Grouper(key='timestamp',freq='M'))
        edits = monthly_data.page_id.count()
        data_edits_pages_monthly.append(
            go.Scatter(
                    x=edits.index,
                    y=edits.data,
                    name=wikis[i]
                    )
        )

    monthly_users = []
    for data in wikis_df:
        monthly_users.append(data.drop_duplicates('contributor_id'))

    for i,wiki in enumerate(wikis):
        monthly_new_users = monthly_users[i].groupby(pd.Grouper(key='timestamp',freq='M')).contributor_id.count()
        data_new_users_monthly.append(
            go.Scatter(
                    x=monthly_new_users.index,
                    y=monthly_new_users.data,
                    name=wiki
                    )
        )


    return html.Div([
            dcc.Graph(
                id='graph-1',
                figure={
                    'data': data_edits_pages_monthly,
                    'layout': {
                        'title': 'Monthly edits'
                    }
                }
            ),
            dcc.Graph(
                id='graph-2',
                figure={
                    'data': data_new_users_monthly,
                    'layout': {
                        'title': 'Monthly new users'
                    }
                }
            )],
        id='graphs'
    )


def generate_main_content():

    wikis_dropdown_options = []
    for index, wiki in enumerate(wikis):
        wikis_dropdown_options.append({'label': wiki, 'value': index})

    metrics_dropdown_options = []
    for index, metric in enumerate(metrics):
        metrics_dropdown_options.append({'label': metric, 'value': index})


    return html.Div(id='main',
        style={'width': '100%'},
        children=[
            html.H1(children='WIKI CHRON', className='container'),
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

                        dcc.RangeSlider(
                            id='dates-slider',
                            min=-5,
                            max=10,
                            step=None,
                            value=[0, 7],
                            disabled=True
                            #~ marks={str(year): str(year) for year in df['year'].unique()}
                        )
                   ]),

            generate_graphs()
        ]
    );



if __name__ == '__main__':
    app = dash.Dash()
    app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
    app.css.append_css({"external_url": "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css"})

    for wiki in wikis:
        wikis_df.append(get_data_from_csv(wiki))

    app.layout = generate_main_content()

    @app.callback(
        Output('graphs', 'children'),
        [Input('wikis-selection-dropdown', 'value'),
        Input('metrics-selection-dropdown', 'value')])
    def update_graphs(selected_wikis, selected_metrics):

        for i in range(len(wikis)):
            if i in selected_wikis:
                data_edits_pages_monthly[i]['visible'] = True
                data_new_users_monthly[i]['visible'] = True
            else:
                data_edits_pages_monthly[i]['visible'] = "legendonly"
                data_new_users_monthly[i]['visible'] = "legendonly"

        graphs = []

        for i, metric in enumerate(metrics):
            if (i in selected_metrics):
                graphs.append(
                    dcc.Graph(
                    id='graph-{}'.format(i),
                    figure={
                        'data': data[i],
                        'layout': {
                            'title': metric
                        }
                    }
                )
                )

        return html.Div(
            id='graphs',
            children=graphs
        )

    app.run_server(debug=True, port=8053)
