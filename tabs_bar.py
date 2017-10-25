import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from loremipsum import get_sentences

app = dash.Dash()

app.scripts.config.serve_locally = True

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


app.layout = html.Div([
    html.Div(
        dcc.Tabs(
            tabs=[
                {'value': 1, 'icon': 'assets/white_graphic.svg'},
                {'value': 2, 'icon': 'assets/white_graphic.svg'},
                {'value': 3, 'icon': 'assets/white_graphic.svg'},
                {'value': 4, 'icon': 'assets/white_graphic.svg'},
            ],
            value=3,
            id='tabs',
            vertical=True,
            style={
                'height': '100vh',
                'borderRight': 'thin lightgrey solid',
                'textAlign': 'left',
                'backgroundColor': '#072146'
            },
            tabsStyle={
                'backgroundColor': '#004481',
                'color': 'white',
                'margin': '5px',
                'borderStyle': 'none'
            }
        ),
        style={'float': 'left'}
    ),
    html.Div(
        html.Div(id='tab-output'),
        style={'width': '95%', 'float': 'right'}
    )
], style={
    'fontFamily': 'Sans-Serif',
    'margin-left': 'auto',
    'margin-right': 'auto',
})


@app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
def display_content(value):
    data = [
        {
            'x': [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                  2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
            'y': [219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                  350, 430, 474, 526, 488, 537, 500, 439],
            'name': 'Rest of world',
            'marker': {
                'color': 'rgb(55, 83, 109)'
            },
            'type': ['bar', 'scatter', 'box'][int(value) % 3]
        },
        {
            'x': [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                  2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
            'y': [16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
                  299, 340, 403, 549, 499],
            'name': 'China',
            'marker': {
                'color': 'rgb(26, 118, 255)'
            },
            'type': ['bar', 'scatter', 'box'][int(value) % 3]
        }
    ]

    return html.Div([
        dcc.Graph(
            id='graph',
            figure={
                'data': data,
                'layout': {
                    'margin': {
                        'l': 30,
                        'r': 0,
                        'b': 30,
                        't': 0
                    },
                    'legend': {'x': 0, 'y': 1}
                }
            }
        ),
        html.Div(' '.join(get_sentences(10)))
    ])


if __name__ == '__main__':
    app.run_server(debug=True)
