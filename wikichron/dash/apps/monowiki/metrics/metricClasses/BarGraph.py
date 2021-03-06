#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
barGraph class.
"""
from ..metric import Metric
from colormap import Colormap
import plotly.graph_objs as go
import numpy as np


class BarGraph(Metric):
    """Class for metrics graphically shown as a bar graph"""

    def __init__(self, code, name, category, func, descp, text):
        """
        Creates a new BarGraph object.

        data -- list of Pandas Series, one per colored bar.
        """
        super(BarGraph, self).__init__(code, name, category, func, descp, text)

        self.data = None
        self.ordered = None


    def set_data(self, metric_data):
        """
        set data to metric_data.
        metric_data -- a list that contains one Pandas Series per colored bar to be shown.
        """
        self.ordered = metric_data.pop(-1)
        self.data = metric_data


    def get_data(self):
        return self.data


    def get_index(self):
        return self.data[0].index


    def get_colors(self, sequencial):
        c = Colormap()
        if sequencial:
            mycmap = c.cmap('YlGnBu')
        else:
            mycmap = c.cmap('tab10')
        rgba = mycmap(np.linspace(0, 1, 256))*255
        long = len(rgba)
        return rgba, long

    def colors_selection(self, sequencial, long, num_submetrics, rgba):
        colors_r = []
        if sequencial == True:
            num_colors = int(long/(num_submetrics+1))
            displace = 0
            for x in range(num_submetrics):
                value = displace + num_colors
                if x%2 == 0:
                    value = value + (x * 10)
                else:
                    value = value + (x * 7)
                valor2 = rgba[value]
                colors_r.append(valor2)
                displace = displace + num_colors
        else:
            value = rgba[0][0]
            colors_r = [rgba[0]]
            #take colors that are apart
            for x in rgba:
               if x[0] != value:
                   colors_r.append(x)
                   value = x[0]
        colors = list(map(lambda x: 'rgb(' + str(int(x[0])) + ', ' + str(int(x[1])) + ', ' + str(int(x[2])) + ')', colors_r))
        return colors

    def draw(self, time_index):

        """
        generate a Bar graph.
        Returns a filled graphs_list.
        """
        graphs_list = []
        num_submetrics = len(self.data)


        for idx in range(num_submetrics):
            graphs_list.append([])

        sequencial = True
        if self.ordered == 0:
            sequencial = False
        rgba, long = self.get_colors(sequencial)
        colors = self.colors_selection(sequencial, long, num_submetrics, rgba)
        for submetric in range(num_submetrics):
            submetric_data = self.data[submetric]

            x_axis = time_index

            if sequencial == False and submetric == 5:
                submetric1 = 9
            else:
                submetric1 = submetric
            graphs_list[submetric] = go.Bar(
                                x=time_index,
                                y=submetric_data,
                                name=submetric_data.name,
                                marker={'color': colors[submetric1]}
                                )
        return graphs_list
