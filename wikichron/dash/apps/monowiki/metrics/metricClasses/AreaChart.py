#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AreaChart class.
"""
from ..metric import Metric 
import plotly.graph_objs as go

class AreaChart(Metric):
    """Class for metrics graphically shown as a filled-area charts"""

    def __init__(self, code, text, category, func, descp):
        """
        Creates a new AreaChart object.

        data -- list of Pandas Series, one per colored bar. 
        """
        super(AreaChart, self).__init__(code, text, category, func, descp)

        self.data = None

    def set_data(self, metric_data):
        """
        set data to metric_data.
        metric_data -- a list that contains one Pandas Series per colored area to be shown.
        """
        self.data = metric_data
    
    def get_index(self):
        return self.data[0].index
    
    def draw(self, is_relative_time):
        """
        generate a filled-area chart.
        Returns a filled graphs_list.
        """
        graphs_list = []
        num_submetrics = len(self.data)

        for idx in range(num_submetrics - 1):
            graphs_list.append([])
        
        for submetric in range(num_submetrics - 1):
                submetric_data = self.data[submetric]
                if is_relative_time:
                    x_axis = list(range(len(submetric_data.index))) # relative to the age of the wiki in months
                else:
                    x_axis = submetric_data.index # natural months
                
                graphs_list[submetric]= go.Scatter(
                                x=x_axis,
                                y=submetric_data,
                                hoverinfo = 'x+y',
                                mode = 'lines',
                                line=dict(width=0.5),
                                stackgroup='one',
                                name=submetric_data.name
                                )
        return graphs_list