#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LineGraph class.
"""
from ..metric import Metric 
import plotly.graph_objs as go

class LineGraph(Metric):
    """Class for metrics graphically shown as line graphs"""

    def __init__(self, code, text, category, func, descp):
        """
        Creates a new LineGraph object.

        data -- A Pandas Series to draw the corresponding line. 
        """
        super(LineGraph, self).__init__(code, text, category, func, descp)

        self.data = None

    def set_data(self, metric_data):
        """
        set data to metric_data.
        """
        self.data = metric_data
    
    def get_index(self):
        return self.data.index

    def draw(self, is_relative_time):
        """
        generate a LineGraph.
        Returns a graphs_list with one scatter graph.
        """
        if is_relative_time:
            x_axis = list(range(len(self.data.index))) # relative to the age of the wiki in months
        else:
            x_axis = self.data.index # natural months
                
        return [go.Scatter(
                        x=x_axis,
                        y=self.data,
                        name=self.data.name
                        )]