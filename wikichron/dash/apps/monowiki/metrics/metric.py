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
    ACTIVE_EDITORS_ANALYSIS = 'Active editors analysis'
    EDITS_ANALYSIS = 'Edits analysis'
    PAGES = 'Pages'
    EDITIONS = 'Edits'
    USERS = 'Users'
    RATIOS = 'Ratios'
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
    def set_data(self, metric_data):
        """
        set the data needed to graphically show each metric, depending on its class.
        """
        pass

    @abstractmethod
    def get_index(self):
        """
        get the index given by the data calculated by the metric.
        """
        pass

    @abstractmethod
    def draw(self, is_relative_time):
        """
        generate the graph associated to each kind of Metric: HeatMap, Bar, AreaChart and Scatter
        """
        pass

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

        for idx in range(num_submetrics - 1):
            graphs_list.append([])
        
        for submetric in range(num_submetrics - 1):
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

class LineGraph(Metric):
    """Class for metrics graphically shown as line graphs"""

    def __init__(self, code, text, category, func, descp):
        """
        Creates a new LineGraph object.

        data -- A list of Pandas Series to draw the corresponding lines -> support both for classic and monowiki. 
        """
        super(LineGraph, self).__init__(code, text, category, func, descp)

        self.data = None

    def set_data(self, metric_data):
        """
        set data to metric_data.
        """
        self.data = metric_data
    
    def get_index(self):
        return self.data[0].index

    def draw(self, is_relative_time):
        """
        generate a LineGraph.
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
                
            graphs_list[submetric] = go.Scatter(
                                x=x_axis,
                                y=submetric_data,
                                name=submetric_data.name
                                )
        return graphs_list





