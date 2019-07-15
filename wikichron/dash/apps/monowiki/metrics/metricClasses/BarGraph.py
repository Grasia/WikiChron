#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
barGraph class.
"""
from ..metric import Metric 
import plotly.graph_objs as go

class BarGraph(Metric):
    """Class for metrics graphically shown as a bar graph"""

    def __init__(self, code, text, category, func, descp):
        """
        Creates a new BarGraph object.

        data -- list of Pandas Series, one per colored bar. 
        """
        super(BarGraph, self).__init__(code, text, category, func, descp)

        self.data = None
    
    def set_data(self, metric_data):
        """
        set data to metric_data.
        metric_data -- a list that contains one Pandas Series per colored bar to be shown.
        """
        self.data = metric_data
    
    def get_index(self):
        return self.data[0].index

    def draw(self, is_relative_time):
        """
        generate a Bar graph.
        Returns a filled graphs_list.
        """
        graphs_list = []
        num_submetrics = len(self.data)

        for idx in range(num_submetrics):
            graphs_list.append([])
        
        for submetric in range(num_submetrics):
            submetric_data = self.data[submetric]

            if is_relative_time:
                x_axis = list(range(len(submetric_data.index))) # relative to the age of the wiki in months
            else:
                x_axis = submetric_data.index # natural months
           
            graphs_list[submetric] = go.Bar(
                                x=x_axis,
                                y=submetric_data,
                                name=submetric_data.name
                                #marker={'color': colors[submetric]}
                                )
        return graphs_list
    