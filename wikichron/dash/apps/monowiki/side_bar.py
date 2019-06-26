#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   side_bar.py

   Descp: The left side bar of WikiChron.

   Created on: 25-oct-2017

   Copyright 2017-2018 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""
# Python built-in imports
import json
import os
import itertools
from warnings import warn
from urllib.parse import urlencode

# Dash framework imports
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import grasia_dash_components as gdc
import dash_html_components as html

# local imports
from .metrics.metric import MetricCategory
from .metrics import interface as interface

# GLOBAL VARIABLES

global app;

global debug;
debug = True if os.environ.get('FLASK_ENV') == 'development' else False

global metric_categories_order;
metric_categories_order = [MetricCategory.ACTIVE_EDITORS_ANALYSIS, MetricCategory.EDITS_ANALYSIS]
category_names = ['ACTIVE_EDITORS_ANALYSIS', 'EDITS_ANALYSIS']

wikis_categories_order = ['SMALL', 'MEDIUM', 'LARGE', 'VERY LARGE']
wikis_categories_descp = ['More than 100 pages', 'More than 1000 pages', 'More than 10k pages', 'More than 10k pages']

# CODE

def fold_button():
    return html.Div(
        html.Div(
            id='fold-img-container',
            className='fold-img-container-cn',
            children=[html.P(id='fold-button')],
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


def generate_metrics_accordion_id(category_name):
    return '{}-metrics'.format(category_name);


def metrics_tab(metrics, selected_metrics):

    def group_metrics_in_accordion(metrics, metric_category,
                                    selected_metrics_value):
        metrics_options = [{'label': metric.text, 'value': metric.code} for metric in metrics]

        # add pre-selected metrics (likely, from url query string),
        # if any, to the accordion which is going to be created.
        if selected_metrics_value:
            metrics_values_checklist = list( set(selected_metrics_value) & set(map(lambda m: m.code, metrics )) ) # take values of pre-selected wikis for this wiki category
        else:
            metrics_values_checklist = []

        metrics_help = [ html.Div(
                            children = html.I(className="fa fa-info-circle checklist-info"),
                            className='one column aside-checklist-option',
                            style={'marginLeft': 'auto'},
                            title=metric.descp
                            )
                        for metric in metrics]

        metrics_help_div = html.Div(children=metrics_help, className='one-column aside-checklist-category')

        return gdc.Accordion(
                    id=generate_metrics_accordion_id(metric_category.name) + '-accordion',
                    className='aside-category',
                    label=metric_category.value,
                    itemClassName='metric-category-label',
                    childrenClassName='metric-category-list',
                    accordionFixedWidth='300',
                    defaultCollapsed=False if metrics_values_checklist else True,
                    children=
                        html.Div(
                            [dcc.Checklist(
                                id=generate_metrics_accordion_id(metric_category.name),
                                className='aside-checklist-category eleven columns',
                                options=metrics_options,
                                values=metrics_values_checklist,
                                labelClassName='aside-checklist-option',
                                labelStyle={'display': 'block'}
                            ),
                            metrics_help_div],
                            className='row'
                        ),
                    style={'display': 'flex'}
                )


    metrics_by_category = interface.get_available_metrics_by_category()

    # Generate accordions containing a checklist following the order
    #   defined by metric_categories_order list.
    metrics_checklist = []
    for category in metric_categories_order:
        metrics_checklist.append(
                group_metrics_in_accordion(
                    metrics_by_category[category],
                    category,
                    selected_metrics
                )
            )

    intro_metrics_paragraph = html.Div(
                html.P(
                    html.Strong('Please, select the charts you wish to see and when you finish click on compare'),
                    className="sidebar-info-paragraph"
                ),
                className="container")

    return html.Div([
        html.Div(
            children = [intro_metrics_paragraph] + metrics_checklist,
            style={'color': 'white'},
            id='metrics-tab-container',
            ),
        ],
        id='metrics-tab'
    );


def compare_button():
    return (
        html.Div(
            html.Button('COMPARE',
                        id='compare-button',
                        className='action-button',
                        type='button',
                        n_clicks=0
            ),
            id='compare-button-container'
        )
    )


def generate_tabs(wikis, metrics, selected_wikis, selected_metrics):
    return (html.Div([
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
                metrics_tab(metrics, selected_metrics)
                ],
            id='side-bar-tabs-container',
        )
    );


def generate_side_bar(wikis, metrics, pre_selected_wikis = [], pre_selected_metrics = []):
    return html.Div(id='side-bar',
        children=[
            fold_button(),
            html.Div(id='side-bar-content',
                children = [
                    generate_tabs(wikis, metrics, pre_selected_wikis, pre_selected_metrics),
                    compare_button(),
                ]
            ),
            gdc.Import(src='/js/side_bar.js')
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

    @app.callback(Output('metrics-tab', 'style'),
               [Input('side-bar-tabs', 'value')]
    )
    def update_metrics_tab_visible(tab_selection):
        if tab_selection == 'metrics':
            return {'display':'block'}
        else:
            return {'display':'none'}

    # Note that we need one State parameter for each category metric that is created dynamically
    @app.callback(Output('url', 'search'),
               [Input('compare-button', 'n_clicks')],
                [State(generate_wikis_accordion_id(name), 'values') for name in wikis_categories_order] +
                [State(generate_metrics_accordion_id(name), 'values') for name in category_names]
    )
    def compare_selection(btn_clicks,
                        wikis_selection_large, wikis_selection_big, wikis_selection_medium, wikis_selection_small,
                        *metrics_selection_l):
        print('Number of clicks: ' + str(btn_clicks))
        if (btn_clicks > 0):
            metrics_selection = list(itertools.chain.from_iterable(metrics_selection_l)) # reduce a list of lists into one list.
            wikis_selection = wikis_selection_large + wikis_selection_big + wikis_selection_medium + wikis_selection_small
            selection = { 'wikis': wikis_selection, 'metrics': metrics_selection}

            query_str = urlencode(selection,  doseq=True)
            return '?' + query_str;


    # simple callbacks to enable / disable 'compare' button
    @app.callback(Output('compare-button', 'disabled'),
                [Input(generate_wikis_accordion_id(name), 'values') for name in wikis_categories_order] +
                [Input(generate_metrics_accordion_id(name), 'values') for name in category_names]
    )
    def enable_compare_button(wikis_selection_large, wikis_selection_big, wikis_selection_medium, wikis_selection_small,
                            *metrics_selection_l):
        metrics_selection = list(itertools.chain.from_iterable(metrics_selection_l)) # reduce a list of lists into one list.
        wikis_selection = wikis_selection_large + wikis_selection_big + wikis_selection_medium + wikis_selection_small
        print ('User selection: {} {}'.format(wikis_selection, metrics_selection))
        if (len(wikis_selection) == 1) and metrics_selection:
            return False
        else:
            return True
    return
