#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AreaChart class.
"""
from ..metric import Metric 
import plotly.graph_objs as go

class AreaChart(Metric):
    """Class for metrics graphically shown as a filled-area charts"""

    def __init__(self, code, name, category, func, descp, text):
        """
        Creates a new AreaChart object.

        data -- list of Pandas Series, one per colored bar. 
        """
        super(AreaChart, self).__init__(code, name, category, func, descp, text)

        self.data = None

    def set_data(self, metric_data):
        """
        set data to metric_data.
        metric_data -- a list that contains one Pandas Series per colored area to be shown.
        """
        self.data = metric_data
		
    def get_data(self):
        return self.data
    
    def get_index(self):
        return self.data[0].index
    
    def draw(self, time_index):
        """
        generate a filled-area chart.
        Returns a filled graphs_list.
        """
        graphs_list = []
        num_submetrics = len(self.data)

        for idx in range(num_submetrics):
            graphs_list.append([])
        
        for submetric in range(num_submetrics):
                submetric_data = self.data[submetric]
                
                graphs_list[submetric]= go.Scatter(
                                x=time_index,
                                y=submetric_data,
                                hoverinfo = 'x+y',
                                mode = 'lines',
                                line=dict(width=0.5),
                                stackgroup='one',
                                name=submetric_data.name
                                )
        return graphs_list