#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LineGraph class.
"""
from ..metric import Metric 
import plotly.graph_objs as go

class LineGraph(Metric):
    """Class for metrics graphically shown as line graphs"""

    def __init__(self, code, name, category, func, descp, text):
        """
        Creates a new LineGraph object.

        data -- A Pandas Series to draw the corresponding line. 
        """
        super(LineGraph, self).__init__(code, name, category, func, descp, text)

        self.data = None

    def set_data(self, metric_data):
        """
        set data to metric_data.
        """
        self.data = metric_data
    
    def get_index(self):
        return self.data.index

    def draw(self, time_index):
        """
        generate a LineGraph.
        Returns a graphs_list with one scatter graph.
        """
                
        return [go.Scatter(
                        x=time_index,
                        y=self.data,
                        name=self.data.name
                        )]