#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   interface.py

   Descp.

   Created on: 14-nov-2017

   Copyright 2017 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

from .metrics import available_metrics as _available_metrics
from .metrics import metrics_dict


def get_available_metrics():
   """ Return a list of the currently available metrics. """
   return _available_metrics

def compute_metrics_on_dataframe(metrics, df):
   """
      Get the requested metrics computed on a dataframe.

      metrics -- list of metric objects
      df -- Dataframe to compute and calculate the metrics on.
      Return a list of panda series corresponding to the provided metrics.
   """
   return [ metric.calculate(df) for metric in metrics ]

def compute_metric_on_dataframes(metric, dfs):
   """
      Get the requested metric computed on given list of dataframes.

      metric -- metric to compute
      dfs -- list of dataframes to compute metric over.
      Return a list of panda series corresponding to the provided metric on different dataframes.
   """
   return [ metric.calculate(df) for df in dfs]

