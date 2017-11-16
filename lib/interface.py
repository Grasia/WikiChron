#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   interface.py

   Descp.

   Created on: 14-nov-2017

   Copyright 2017 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

from metrics import available_metrics

def get_available_metrics():
   """ Return a list of the currently available metrics. """
   return available_metrics

def get_metrics(metrics, df):
   """
      Get the requested metrics computed on a dataframe.

      codes -- list of metric objects
      df -- Dataframe to compute and calculate the metrics on.
      Return a list of panda series corresponding to the provided metrics.
   """
   return 0

