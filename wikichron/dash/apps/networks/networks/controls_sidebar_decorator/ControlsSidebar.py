"""
   ControlsSidebar.py

   Descp: A class to implement the decorator pattern in order to make an
     easier implementation of the right sidebar

   Created on: 08-02-2019

   Copyright 2019 Youssef 'FRYoussef' El Faqir el Rhazoui <f.r.youssef@hotmail.com>
"""

import abc
import dash_html_components as html
import grasia_dash_components as gdc


class ControlsSidebar(metaclass=abc.ABCMeta):

    def __init__(self):
        self.html_sidebar = []
        self.stats_section = []
        self.options_section = []


    def fold_button(self):
        return html.Div(
            html.Div(
                id='controls-fold-img-container',
                className='fold-img-container-cn',
                children=[
                    html.P(id='controls-fold-button', className='fold-button-cn')
                ],
            ),
            id='controls-fold-container',
            style={
                'display': 'flex'
            }
        );


    def add_stats_section(self, html_stats):
        self.stats_section = html.Div([
                    html.H5('Network Stats', className='control-title'),
                    html.Div(id='stats', className='stats-container', children=[])
                    ],
                    className='control-container')
        self.stats_section.children[1].children = html_stats


    def add_options_section(self, html_options):
        self.options_section = html.Div([
                    html.H5('Network Options', className='control-title'),
                    html.Div(children=[])
                ], className='control-container')
        self.options_section.children[1].children = html_options


    def add_all_sections(self, html_stats, html_options):
        self.add_stats_section(html_stats)
        self.add_options_section(html_options)


    def build(self):
        self.html_sidebar = html.Div(id='controls-sidebar-wrapper',
                            children=[
                                html.Div(id='controls-side-bar',
                                    className='side-bar-cn',
                                    children=[
                                        self.fold_button(),
                                        html.Div(id='controls-side-bar-content',
                                            children=[
                                                self.stats_section,
                                                self.options_section
                                            ]),
                                        gdc.Import(src='/js/controls_side_bar.js')
                                    ])
                            ],
                            style={
                                'display': 'flex',
                                'flexDirection': 'row-reverse'
                            }
                        );

        return self.html_sidebar
