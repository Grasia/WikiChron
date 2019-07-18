#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   interface.py

   Descp.

   Created on: 14-nov-2017

   Copyright 2017-2018 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

import numpy as np
import time
import os

from .monowiki_stats import calculate_index_all_months
from . import metrics_generator

print('Generating available metrics...')
_available_metrics = metrics_generator.generate_metrics()
_metrics_dict_by_code = metrics_generator.generate_dict_metrics(_available_metrics)
_metrics_by_category = metrics_generator.generate_dict_metrics_by_category(_available_metrics)


def get_available_metrics():
    """ Return a list of the currently available metrics. """
    return _available_metrics


def get_available_metrics_dict():
    """
Return a dictionary of the currently available metrics where the metric
 codes are the keys and the values are the corresponding metric object.
    """
    return _metrics_dict_by_code


def get_available_metrics_by_category():
    """
Return a dictionary where every key is a MetricCategory object and every value
 is a list of all the available wikis which belong to that category
    """
    return _metrics_by_category


def compute_metrics_on_dataframe(metrics, df):
    """
        Get the requested metrics computed on a dataframe in relative dates.

        metrics -- list of metric objects
        df -- Dataframe to compute and calculate the metrics on.
        Return a list of panda series corresponding to the provided metrics.
    """
    index = calculate_index_all_months(df) #TOIMPROVE
    #metrics_data = []
    for metric in metrics:
        metric_series = metric.calculate(df, index)
        metric.set_data(metric_series)
        #~ metric_series.name = '{}<>{}'.format(df.index.name,metric.code) #TOFIX for monowiki metrics
        #metrics_data.append(metric_series)
    return metrics


def compute_data(dataframes, metrics):
    """
        One wiki only, so one dimensional array where every element
        is a pandas dataframe with the computed metric.
    """
    return compute_metrics_on_dataframe(metrics, dataframes)


# Too inefficient with the current implementation
# TOIMPROVE
# NOTBEENUSED
#~ def compute_metric_on_dataframes(metric, dfs):
    #"""
      #Get the requested metric computed on given list of dataframe in
      #absolute dates.

      #metric -- metric to compute
      #dfs -- list of dataframes to compute metric over.
      #Return a list of panda series corresponding to the provided metric
      #on different dataframes.
    #"""
   #~ return [ metric.calculate(df) for df in dfs]

