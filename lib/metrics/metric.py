#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   metric_class.py

   Descp.

   Created on: 14-nov-2017

   Copyright 2017 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

from enum import Enum, unique
@unique
class MetricCategory(Enum):
    PAGES = 'New Pages'
    EDITIONS = 'Edits'
    USERS = 'Users'
    RATIOS = 'Ratios'
    DISTRIBUTION = 'Distribution of Participation'

class Metric:
    """ Class for ADT Metric. """

    def __init__(self, code, text, category, func, descp):
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

