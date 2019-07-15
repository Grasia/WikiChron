#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HeatMap class.
"""
from ..metric import Metric 
import plotly.graph_objs as go
class HeatMap(Metric):
    """Class for metrics graphically shown as heatmaps"""
    
    def __init__(self, code, text, category, func, descp):
        """
        Creates a new HeatMmap object.

        xaxis -- The horizontal axis in the HeatMap (time index).
        yaxis -- The vertical axis in the HeatMap.
        zaxis -- The color dimension.s
        """
        super(HeatMap, self).__init__(code, text, category, func, descp)

        self.xaxis = None
        self.yaxis = None
        self.zaxis = None
    

    def set_data(self, metric_data):
        """
        Set xaxis, yaxis and zaxis.
        metric_data[0] -- x axis (time index).
        metric_data[1] -- y axis.
        metric_data[2] -- z axis.
        """
        self.xaxis = metric_data[0]
        self.yaxis = metric_data[1]
        self.zaxis = metric_data[2]

    def get_index(self):
        return self.xaxis

    def draw(self, is_relative_time):
        """
        generate a HeatMap graph.
        returns a filled graph_list.
        """
        if is_relative_time:
            x_axis = list(range(len(self.xaxis))) # relative to the age of the wiki in months
        else:
            x_axis = self.xaxis # natural months

        return [go.Heatmap(z=self.zaxis,
                        x=x_axis,
                        y=self.yaxis,
                        colorscale= 'Viridis'
                        )]
