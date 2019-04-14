#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   data_controller.py

   Descp: A file with functions which intermediate between the data and the
WikiChron code.

   Created on: 15-feb-2019

   Copyright 2018-2019 Youssef 'FRYoussef' El Faqir El Rhazoui <f.r.youssef@hotmail.com>
"""

# Built-in imports
import pandas as pd
import os
import numpy as np
import time
from datetime import datetime
from warnings import warn
import json

# Local imports:
from .networks import interface

# get csv data location (data/ by default)
global data_dir;
global precooked_net_dir;
data_dir = os.getenv('WIKICHRON_DATA_DIR', 'data')
precooked_net_dir = os.getenv('PRECOOKED_NETWORK_DIR', 'precooked_data/networks')

### CACHED FUNCTIONS ###

def set_cache(cache):

    # we need to declare as *global* all the cached functions we want to be
    #  available to be used from outside of this file.
    global read_data
    global get_network

    @cache.memoize()
    def read_data(wiki):
        df = get_dataframe_from_csv(wiki['data'])
        prepare_data(df)
        df = clean_up_bot_activity(df, wiki)
        return df


    @cache.memoize(timeout=3600)
    def get_network(wiki, network_code, lower_bound = '', upper_bound = ''):
        """
        Parameters
            - wiki: Related info about the wiki selected.
            - network_code: network selected. It is an instance of BaseNetwork.
            - lower_bound: a formated string "%Y-%m-%d %H:%M:%S", to filter the pandas obj
            - upper_bound: a formated string "%Y-%m-%d %H:%M:%S", to filter the pandas obj
        Return: Data representing the network.
        """
        # load data from csvs:
        time_start_loading_csvs = time.perf_counter()
        df = read_data(wiki)
        time_end_loading_csvs = time.perf_counter() - time_start_loading_csvs
        print(' * [Timing] Loading csvs : {} seconds'.format(time_end_loading_csvs) )

        network = interface.factory_network(network_code, wiki['name'])
        print(' * [Info] Starting calculations....')
        time_start_calculations = time.perf_counter()
        network.build_network(df=df, lower_bound = lower_bound, upper_bound = upper_bound)
        time_end_calculations = time.perf_counter() - time_start_calculations
        print(' * [Timing] Calculations : {} seconds'.format(time_end_calculations) )
        return network


### OTHER DATA-RELATED FUNCTIONS ###

def get_available_wikis():
    wikis_json_file = open(os.path.join(data_dir, 'wikis.json'))
    wikis = json.load(wikis_json_file)
    return wikis


def get_first_entry(wiki):
    return wiki['first_edit']['date']


def get_last_entry(wiki):
    return wiki['last_edit']['date']


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


def get_dataframe_from_csv(csv):
    """ Read and parse a csv and return the corresponding pandas dataframe"""

    print('Loading csv for ' + csv)
    time_start_loading_one_csv = time.perf_counter()
    df = pd.read_csv(os.path.join(data_dir, csv),
                    delimiter=',', quotechar='|',
                    index_col=False)
    df['timestamp']=pd.to_datetime(df['timestamp'],format='%Y-%m-%dT%H:%M:%SZ')
    print('!!Loaded csv for ' + csv)
    time_end_loading_one_csv = time.perf_counter() - time_start_loading_one_csv
    print(' * [Timing] Loading {} : {} seconds'
                    .format(csv, time_end_loading_one_csv))
    df.index.name = csv
    return df


def clean_up_bot_activity(df, wiki):
    if 'bots' in wiki:
        botsids = [bot['id'] for bot in wiki['bots']]
        return remove_bots_activity(df, botsids)
    else:
        warn("Warning: Missing information of bots ids. Note that graphs can be polluted of non-human activity.")
    return df


def get_bot_names(wiki: dict) -> set:
    wikis_json_file = open(os.path.join(data_dir, 'wikis.json'))
    wikis = json.load(wikis_json_file)
    di_wiki = {}
    for i in range(len(wikis)):
        if wikis[i]['name'] == wiki:
            di_wiki = wikis[i]
            break

    if not di_wiki or 'bots' not in di_wiki:
        return {}

    return {bot['name'] for bot in di_wiki['bots']}


def calculate_indices_all_months(wiki):
    data = read_data(wiki)
    monthly_data_align_begining = data.groupby(pd.Grouper(key='timestamp', freq='MS'))
    monthly_data_align_end = data.groupby(pd.Grouper(key='timestamp', freq='M'))
    begining_index = monthly_data_align_begining.size().index
    end_index = monthly_data_align_end.size().index
    return (begining_index, end_index)


def parse_int_to_timestamp(time):
    return datetime.utcfromtimestamp(int(time)).strftime("%Y-%m-%d")


def parse_timestamp_to_int(time):
    return int(datetime.timestamp(datetime.strptime(str(time), "%Y-%m-%d")))
