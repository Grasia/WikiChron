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