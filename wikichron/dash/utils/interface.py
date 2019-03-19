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

from .metrics import available_metrics as _available_metrics
from .metrics import metrics_dict
from .metrics import stats

def get_available_metrics():
    """ Return a list of the currently available metrics. """
    return _available_metrics


def compute_metrics_on_dataframe(metrics, df):
    """
        Get the requested metrics computed on a dataframe in relative dates.

        metrics -- list of metric objects
        df -- Dataframe to compute and calculate the metrics on.
        Return a list of panda series corresponding to the provided metrics.
    """
    index = stats.calculate_index_all_months(df) #TOIMPROVE
    metrics_data = []
    for metric in metrics:
        metric_series = metric.calculate(df, index)
        metric_series.name = '{}<>{}'.format(df.index.name,metric.code)
        metrics_data.append(metric_series)
    return metrics_data


def compute_data(dataframes, metrics):
    """ Load analyzed data by every metric for every dataframe and return it in two dimensional array """

    metrics_by_wiki = []
    for df in dataframes:
        metrics_by_wiki.append(compute_metrics_on_dataframe(metrics, df))

    # transposing matrix row=>wikis, column=>metrics to row=>metrics, column=>wikis
    wiki_by_metrics = []
    for metric_idx in range(len(metrics)):
        metric_row = [metrics_by_wiki[wiki_idx].pop(0) for wiki_idx in range(len(metrics_by_wiki))]
        wiki_by_metrics.append(metric_row)

    return wiki_by_metrics


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

