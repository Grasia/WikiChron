#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   metric_class.py

   Descp.

   Created on: 14-nov-2017

   Copyright 2017-2019 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""
import plotly.graph_objs as go
from abc import ABC, abstractmethod
from enum import Enum, unique
@unique
class MetricCategory(Enum):
    ACTIVE_USER_DISTRIBUTION = 'Active users distribution'
    EDIT_DISTRIBUTION = 'Edits distribution'
    PAGES = 'Pages'
    EDITIONS = 'Edits'
    USERS = 'Users'
    RATIOS = 'Ratios'
    RETENTION = 'Retention'
    DISTRIBUTION = 'Distribution of Participation'

class Metric(ABC):
    """ Class for ADT Metric. """

    def __init__(self, code, text, category, func, descp):
        """
        Creates a new Metric object.

        code -- an unique string id for this metric.
        text -- title of the metric to display in the UI selection list
        category -- MetricCategory this metric belongs to
        (see MetricCategory Enum).
        func -- Python function to call to compute this metric.
        Presumably, located in the stats.py file.
        descp -- Short description (about a paragraph) of what
        the metric consists in.
        Return a new Metric instance.
        """
        self.code = code
        self.text = text
        self.category = category
        self.func = func
        self.descp = descp

        super().__init__()


    def calculate(self, pandas_data_frame, index=None):
        """
        Calculate the metric data using the pandas_data_frame.

        Return a pandas series
        """
        return self.func(pandas_data_frame, index)

    @abstractmethod
    def show(self, metric_data, is_relative_time):
        """
        generate the graph associated to each kind of Metric: HeatMap, Bar, AreaChart and Scatter
        """
        pass

class HeatMap(Metric):
    """Class for metrics graphically shown as heatmaps"""
    
    def show(self, metric_data, is_relative_time):
        """
        generate a HeatMap graph using metric_data.
        metric_data[0] -- x axis.
        metric_data[1] -- y axis.
        metric_data[2] -- z axis.

        returns a filled graph_list.
        """
        if is_relative_time:
            x_axis = list(range(len(metric_data[0]))) # relative to the age of the wiki in months
        else:
            x_axis = metric_data[0] # natural months

        y_axis = metric_data[1]
        z_axis = metric_data[2]

        return go.Heatmap(z=z_axis,
                        x=x_axis,
                        y=y_axis,
                        colorscale= 'Viridis'
                        )

class BarGraph(Metric):
    """Class for metrics graphically shown as a bar graph"""

    def show(self, metric_data, is_relative_time):
        """
        generate a Bar graph using metric_data.
        metric_data is an array which contains a Pandas Series per colored bar.
        Returns a filled graphs_list.
        """
        graphs_list = []
        num_submetrics = len(metric_data)
        for submetric in range(num_submetrics):
                submetric_data = metric_data[submetric]
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
    
class AreaChart(Metric):
    """Class for metrics graphically shown as a filled-area charts"""

    def show(self, metric_data, is_relative_time):
        """
        generate a filled-area chart using metric_data.
        metric_data is an array which contains a Pandas Series per area.
        Returns a filled graphs_list.
        """
        graphs_list = []
        num_submetrics = len(metric_data)
        num_submetrics = len(metric_data)
        for submetric in range(num_submetrics):
                submetric_data = metric_data[submetric]
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

class LineGraph(Metric):
    """Class for metrics graphically shown as line graphs"""
    def show(self, metric_data, is_relative_time):
        """
        generate a filled-area chart using metric_data.
        metric_data is an array which contains a Pandas Series per area.
        Returns a filled graphs_list.
        """
        graphs_list = []
        num_submetrics = len(metric_data)
        for submetric in range(num_submetrics):
            submetric_data = metric_data[submetric]
            if is_relative_time:
                x_axis = list(range(len(submetric_data.index))) # relative to the age of the wiki in months
            else:
                x_axis = submetric_data.index # natural months
            graphs_list[submetric] = go.Scatter(
                                x=x_axis,
                                y=submetric_data,
                                name=submetric_data.name
                                )
        return graphs_list





