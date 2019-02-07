#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   side_bar.py

   Descp: The left side bar of WikiChron.

   Created on: 25-oct-2017

   Copyright 2017-2018 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

import json
import os
import itertools
from warnings import warn
from urllib.parse import urlencode

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import grasia_dash_components as gdc
import dash_html_components as html

# GLOBAL VARIABLES

global app;

global debug;
debug = True if os.environ.get('FLASK_ENV') == 'development' else False

wikis_categories_order = ['SMALL', 'MEDIUM', 'LARGE', 'VERY LARGE']
wikis_categories_descp = ['More than 100 pages', 'More than 1000 pages', 'More than 10k pages', 'More than 10k pages']

# CODE

def fold_button():
    return html.Div(
        html.Div(
            id='fold-img-container',
            className='fold-img-container-cn',
            children=[
                html.P(id='fold-button', className='fold-button-cn')
            ],
        ),
        id='fold-container',
        style={
            'display': 'flex',
            'flexDirection': 'row-reverse'
        }
    );


def generate_wikis_accordion_id(category_name):
    return '{}-wikis'.format(category_name);


def wikis_tab(wikis, selected_wikis):

    def group_wikis_in_accordion(wikis, wikis_category, wiki_category_descp,
                                selected_wikis_value):

        wikis_options = [{'label': wiki['name'], 'value': wiki['url']} for wiki in wikis]

        # add pre-selected wikis (likely, from url query string),
        # if any, to the accordion which is going to be created.
        if selected_wikis_value:
            wikis_values_checklist = list( set(selected_wikis_value) & set(map(lambda w: w['url'], wikis )) ) # take values (url) of pre-selected wikis for this wiki category
        else:
            wikis_values_checklist = []


        return gdc.Accordion(
                    id=generate_wikis_accordion_id(wikis_category) + '-accordion',
                    className='aside-category',
                    label=wikis_category,
                    itemClassName='metric-category-label',
                    childrenClassName='metric-category-list',
                    accordionFixedWidth='300',
                    defaultCollapsed=False if wikis else True,
                    children=[
                        html.Strong(wiki_category_descp, style={'fontSize': '14px'}),
                        dcc.Checklist(
                            id=generate_wikis_accordion_id(wikis_category),
                            className='aside-checklist-category',
                            options=wikis_options,
                            values=wikis_values_checklist,
                            labelClassName='aside-checklist-option',
                            labelStyle={'display': 'block'}
                        )
                    ],
                    style={'display': 'flex'}
                )

    # group metrics in a dict w/ key: category, value: [wikis]
    wikis_by_category = {wiki_category: [] for wiki_category in wikis_categories_order}
    for wiki in wikis:

        if wiki['pages'] > 100000:
            wikis_by_category['VERY LARGE'].append(wiki)
        elif wiki['pages'] > 10000:
            wikis_by_category['LARGE'].append(wiki)
        elif wiki['pages'] > 1000:
            wikis_by_category['MEDIUM'].append(wiki)
        else:
            wikis_by_category['SMALL'].append(wiki)

    # Generate accordions containing a checklist following the order
    #   defined by metric_categories_order list.
    wikis_checklist = []
    for (category, category_descp) in zip(wikis_categories_order, wikis_categories_descp):
        wikis_checklist.append(
                group_wikis_in_accordion(
                    wikis_by_category[category],
                    category,
                    category_descp,
                    selected_wikis
                )
            )

    intro_wikis_paragraph = html.Div(
                html.P(
                    html.Strong(('You can compare between {} wikis').format(len(wikis))),
                    className="sidebar-info-paragraph"
                ),
                className="container")

    return html.Div([
        html.Div(
            children = [intro_wikis_paragraph] + wikis_checklist,
            style={'color': 'white'},
            id='wikis-tab-container',
            ),
        ],
        id='wikis-tab'
    );


def networks_tab(networks, selected_network):

    networks_options = [{'label': nw.NAME, 'value': nw.CODE} for nw in networks]

    default_network = selected_network if selected_network else networks[0].CODE

    networks_checklist = html.Div(
                           [dcc.RadioItems(
                                id='network-selection',
                                className='aside-checklist-category eleven columns',
                                options=networks_options,
                                value=default_network,
                                labelClassName='aside-checklist-option',
                                labelStyle={'display': 'block'}
                            )],
                            className='container row',
                            style={'display': 'flex'}
                        );

    intro_networks_paragraph = html.Div(
                html.P(
                    html.Strong('Select a network type from the list:'),
                    className="sidebar-info-paragraph"
                ),
                className="container")

    return html.Div([
        html.Div(
            children = [
                intro_networks_paragraph,
                networks_checklist,
            ],
            style={'color': 'white'},
            id='networks-tab-container',
            ),
        ],
        id='networks-tab'
    );


def compare_button():
    return (
        html.Div(
            html.Button('GENERATE',
                        id='compare-button',
                        className='action-button',
                        type='button',
                        n_clicks=0
            ),
            id='compare-button-container',
            className='compare-button-container-cn'
        )
    )


def generate_tabs(wikis, networks, selected_wikis, selected_network):
    return (html.Div([
                gdc.Tabs(
                    tabs=[
                        {'value': 'wikis', 'label': 'WIKIS'},
                        {'value': 'networks', 'label': 'NETWORKS'}
                    ],
                    value='wikis',
                    id='side-bar-tabs',
                    vertical=False,
                    selectedTabStyle={
                        'backgroundColor': '#004481',
                    },
                    selectedTabClassName='side-bar-selected-tab',
                    style={
                        'width': '100%',
                        'textAlign': 'center',
                        'border': 'none',
                    },
                    tabsStyle={
                        'backgroundColor': '#072146',
                        'borderRadius': '3px',
                        'borderLeftStyle': 'none',
                        'borderRightStyle': 'none',
                    },
                    tabsClassName='side-bar-tab',
                ),
                wikis_tab(wikis, selected_wikis),
                networks_tab(networks, selected_network)
                ],
            id='side-bar-tabs-container',
        )
    );


def generate_side_bar(wikis, networks, pre_selected_wikis = [], pre_selected_network = None):
    return html.Div(id='side-bar',
        children=[
            fold_button(),
            html.Div(id='side-bar-content',
                children = [
                    generate_tabs(wikis, networks, pre_selected_wikis, pre_selected_network),
                    compare_button(),
                ]
            ),
            gdc.Import(src='js/side_bar.js')
        ]
    );


def bind_callbacks(app):


    @app.callback(Output('wikis-tab', 'style'),
                   [Input('side-bar-tabs', 'value')]
    )
    def update_wikis_tab_visible(tab_selection):
        if tab_selection == 'wikis':
            return {'display':'block'}
        else:
            return {'display':'none'}

    @app.callback(Output('networks-tab', 'style'),
               [Input('side-bar-tabs', 'value')]
    )
    def update_networks_tab_visible(tab_selection):
        if tab_selection == 'networks':
            return {'display':'block'}
        else:
            return {'display':'none'}

    # Note that we need one State parameter for each category metric that is created dynamically
    @app.callback(Output('url', 'search'),
               [Input('compare-button', 'n_clicks')],
                [State(generate_wikis_accordion_id(name), 'values') for name in wikis_categories_order] +
                [State('network-selection', 'value')]
    )
    def compare_selection(btn_clicks,
                        wikis_selection_large, wikis_selection_big, wikis_selection_medium, wikis_selection_small,
                        network_selection):
        print('Number of clicks: ' + str(btn_clicks))
        if (btn_clicks > 0):
            wikis_selection = wikis_selection_large + wikis_selection_big + wikis_selection_medium + wikis_selection_small
            selection = { 'wikis': wikis_selection, 'network': network_selection}

            query_str = urlencode(selection,  doseq=True)
            return '?' + query_str;


    # simple callbacks to enable / disable 'compare' button
    @app.callback(Output('compare-button', 'disabled'),
                [Input(generate_wikis_accordion_id(name), 'values') for name in wikis_categories_order] +
                [Input('network-selection', 'value')]
    )
    def enable_compare_button(wikis_selection_large, wikis_selection_big, wikis_selection_medium, wikis_selection_small,
                            network_selection):
        wikis_selection = wikis_selection_large + wikis_selection_big + wikis_selection_medium + wikis_selection_small
        print ('User selection: {} {}'.format(wikis_selection, network_selection))
        if wikis_selection and network_selection:
            if len(wikis_selection) > 1:
                return True
            return False
        else:
            return True
    return

if __name__ == '__main__':

    print('Using version ' + dcc.__version__ + ' of Dash Core Components.')
    print('Using version ' + gdc.__version__ + ' of Grasia Dash Components.')

    global app;

    app = dash.Dash()

    app.scripts.config.serve_locally = True

#~ app.scripts.append_script({ "external_url": "app.js"})
    from app import get_available_wikis
    available_wikis = get_available_wikis('data/')

    from lib.interface import get_available_networks
    app.layout = html.Div(id='app-layout',
        style={'display': 'flex'},
        children=[
            generate_side_bar(available_wikis, get_available_networks()),
        ]
    );
    #~ bind_callbacks(app)

    app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
    app.css.append_css({"external_url": "https://codepen.io/akronix/pen/rpQgqQ.css"})

    app.run_server(port=8052, debug=True)

