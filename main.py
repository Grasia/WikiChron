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

wikis = ['recipes', 'eslagunanegra_pages_full', 'cocktails', 'zelda']

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

    wikis_data = []
    for wiki in wikis:
        wikis_data.append(get_data_from_csv(wiki))

    data_edits_pages_monthly = []
    for i, data in enumerate(wikis_data):
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
    for data in wikis_data:
        monthly_users.append(data.drop_duplicates('contributor_id'))

    data_new_users_monthly = []
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
                                options=[
                                    {'label': 'Wikipedia', 'value': '1'},
                                    {'label': 'Wiki 4', 'value': '2'},
                                    {'label': 'Wiki 5', 'value': '3'}
                                ],
                                multi=True,
                                searchable=False,
                                value="1,2,3"
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
                                options=[
                                    {'label': 'Total per user', 'value': '1'},
                                    {'label': 'Metric 3', 'value': '2'},
                                    {'label': 'Metric 4', 'value': '3'},
                                    {'label': 'Metric 5', 'value': '4'}
                                ],
                                multi=True,
                                searchable=False,
                                value="1,2,3,4"
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
                            count=1,
                            min=-5,
                            max=10,
                            step=0.5,
                            value=[-3, 7]
                        )
                   ]),

            generate_graphs()
        ]
    );

#@app.callback(
    #dash.dependencies.Output('graph-with-slider', 'figure'),
    #[dash.dependencies.Input('year-slider', 'value')])
#def update_figure(selected_year):
    #filtered_df = df[df.year == selected_year]
    #traces = []
    #for i in filtered_df.continent.unique():
        #df_by_continent = filtered_df[filtered_df['continent'] == i]
        #traces.append(go.Scatter(
            #x=df_by_continent['gdpPercap'],
            #y=df_by_continent['lifeExp'],
            #text=df_by_continent['country'],
            #mode='markers',
            #opacity=0.7,
            #marker={
                #'size': 15,
                #'line': {'width': 0.5, 'color': 'white'}
            #},
            #name=i
        #))

    #return {
        #'data': traces,
        #'layout': go.Layout(
            #xaxis={'type': 'log', 'title': 'GDP Per Capita'},
            #yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
            #margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            #legend={'x': 0, 'y': 1},
            #hovermode='closest'
        #)
    #}


if __name__ == '__main__':
    app = dash.Dash()
    app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
    app.css.append_css({"external_url": "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css"})
    app.layout = generate_main_content()
    app.run_server(debug=True, port=8053)
