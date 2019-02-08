"""
   CoEditingControlsSidebarDecorator.py

   Descp: A class to implement the decorator pattern in order to make an
     easier implementation of the right sidebar

   Created on: 08-02-2019

   Copyright 2019 Youssef 'FRYoussef' El Faqir el Rhazoui <f.r.youssef@hotmail.com>
"""

import abc
import dash_html_components as html
from .BaseControlsSidebarDecorator import BaseControlsSidebarDecorator

class CoEditingControlsSidebarDecorator(BaseControlsSidebarDecorator):

    def __init__(self, sidebar):
        super().__init__(sidebar)


    def add_stats_section(self):
        super().add_stats_section()

        stats = [
            html.Div([
                html.P('Nodes: ...', className='left-element'),
                html.P('First User: ...', className='right-element')
            ]),
            html.Div([
                html.P('Edges: ...', className='left-element'),
                html.P('Last User: ...', className='right-element')
            ]),
            html.Div([
                html.P('Communities: ...', className='left-element', id='n_communities'),
                html.P('Max Hub Degree: ...', className='right-element')
            ])]

        self.add_stats(stats)


    def add_metrics_section(self):
        super().add_metrics_section()

        metrics = [
                html.Div(children=[
                    html.Span('PageRank', className='left-element'),
                    html.Button('Run', id='calculate_page_rank',
                                type='button',
                                className='right-element action-button'),
                    ],
                    className='metrics-section'),
                html.Div([
                    html.Span('Communities', className='left-element'),
                    html.Button('Run', id='calculate_communities',
                                type='button',
                                className='right-element action-button')
                ],
                className='metrics-section')
            ]

        self.add_metrics(metrics)


    def add_options_section(self):
        super().add_options_section()

        options = [
                    html.Button('Show Labels', id='show_labels',
                        className='control-button action-button'),
                    html.Button('Show PageRank', id='show_page_rank',
                        className='control-button action-button'),
                    html.Button('Color by Cluster', id='color_cluster',
                        className='control-button action-button'),
                ]

        self.add_options(options)


    def add_all_sections(self):
        self.add_stats_section()
        self.add_metrics_section()
        self.add_options_section()