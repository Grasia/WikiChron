# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

app = dash.Dash()

app.layout = html.Div(children=[
   html.H1(children='WIKI NAME'),
   html.Hr(),

   html.Div(id='selection-div',
      className='container',
      children=[
         html.Div(id='first-row',
            className='row',
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
                        className='six columns',
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

        html.Div(id='metrics-selection-div', className='row', children=[
            html.P(className='three columns'),
            html.Strong('Metrics:', className='two columns', style={'marginLeft': '0'}),

            dcc.Dropdown(
                id='metrics-selection-dropdown',
                className='six columns',
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

    html.Div(id='date-slider-div', children=[

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

    dcc.Graph(
        id='graph-1',
        figure={
            'data': [
                go.Scatter(
                    x=[1, 2, 3],
                    y=[2, 4, 5],
                    name='value'
                )
            ],
            'layout': {
                'title': 'Monthly new users'
            }
        }
    )
]);

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
app.css.append_css({"external_url": "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css"})

if __name__ == '__main__':
    app.run_server(debug=True)
