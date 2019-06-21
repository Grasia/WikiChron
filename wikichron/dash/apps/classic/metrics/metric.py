#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   metric_class.py

   Descp.

   Created on: 14-nov-2017

   Copyright 2017-2018 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

from enum import Enum, unique
@unique
class MetricCategory(Enum):
    PAGES = 'Pages'
    EDITIONS = 'Edits'
    USERS = 'Users'
    RATIOS = 'Ratios'
    RETENTION = 'Retention'
    DISTRIBUTION = 'Distribution of Participation'

class Metric:
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


    def calculate(self, pandas_data_frame, index=None):
        """
        Calculate the metric data using the pandas_data_frame.

        Return a pandas series
        """
        return self.func(pandas_data_frame, index)

