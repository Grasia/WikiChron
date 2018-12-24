#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   interface.py

   Descp.

   Created on: 14-nov-2017

   Copyright 2017-2018 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>, 
                      Youssef El Faqir El Rhazoui 
"""

import numpy as np

from .metrics import available_metrics as _available_metrics
from .metrics import metrics_dict
from .metrics import stats
from .networks import available_networks as _available_networks
import os
import pandas as pd
import time
from warnings import warn

global data_dir;
data_dir = os.getenv('WIKICHRON_DATA_DIR', 'data')

def get_available_metrics():
   """ Return a list of the currently available metrics. """
   return _available_metrics

def get_available_networks():
   """ Return a list of the currently available networks. """
   return _available_networks

def remove_bots_activity(df, bots_ids):
   """
      Filter out bots activity from pandas dataframe.

      df -- data to be filtered. It'll be modified in place
      bots_ids -- numpy array with the userid for every bot
      Return a dataframe derived from the original but with all the
         editions made by bot users removed
   """
   bots = np.array(bots_ids)
   return df[~df['contributor_id'].isin(bots)]

def prepare_data(df):
   """
      Prepare data in the correct input format for the metric
      calculation functions.

      df -- data to be prepared.
      Modifies inplace the input data as well as returns that data
      in the appropiate format for further calling of metric functions.
   """
   return df.sort_values(by='timestamp', inplace=True)


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

# Too inefficient with the current implementation
# TOIMPROVE
# NOTBEENUSED
#~ def compute_metric_on_dataframes(metric, dfs):
   """
      Get the requested metric computed on given list of dataframe in
      absolute dates.

      metric -- metric to compute
      dfs -- list of dataframes to compute metric over.
      Return a list of panda series corresponding to the provided metric
      on different dataframes.
   """
   #~ return [ metric.calculate(df) for df in dfs]

def get_dataframe_from_csv(csv):
    """ Read and parse a csv and return the corresponding pandas dataframe"""
    print('Loading csv for ' + csv)
    time_start_loading_one_csv = time.perf_counter()
    df = pd.read_csv(os.path.join(data_dir, csv),
                    delimiter=';', quotechar='|',
                    index_col=False)
    df['timestamp']=pd.to_datetime(df['timestamp'],format='%Y-%m-%dT%H:%M:%SZ')
    #~ df.set_index(df['timestamp'], inplace=True) # generate a datetime index
    #~ print(df.info())
    print('!!Loaded csv for ' + csv)
    time_end_loading_one_csv = time.perf_counter() - time_start_loading_one_csv
    print(' * [Timing] Loading {} : {} seconds'
                    .format(csv, time_end_loading_one_csv))
    df.index.name = csv
    return df


def clean_up_bot_activity(df, wiki):
    if 'botsids' in wiki:
        return remove_bots_activity(df, wiki['botsids'])
    else:
        warn("Warning: Missing information of bots ids. Note that graphs can be polluted of non-human activity.")
    return df


def get_network_from_bin(name, network_t):
    """
    Find and read a network from a bin file

    Parameters: 
      - name: the network name
      - network_t: the network type

    Return:
      - 0 if the file doesn't exist
      - An network_t type instance if it exist

    Raise Exception:
      - network_t is not avaliable
    """
    