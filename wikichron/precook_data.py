#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   generate_wiki_network.py

   Descp: This script generates a network per wiki csv. It get them from ../data
    and creates a bin network in precooked_data/networks

   Created on: 17-dic-2018

   Copyright 2018 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
   Copyright 2018 Youssef El Faqir El Rhazoui <f.r.youssef@hotmail.com>


   Distributed under the terms of the AGPLv3 license.
"""


import os
from os.path import join
import sys
import pandas as pd
import json
import time

import lib.interface as lib
from lib.networks.types.CoEditingNetwork import CoEditingNetwork

if not 'WIKICHRON_DATA_DIR' in os.environ:
    os.environ['WIKICHRON_DATA_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')
data_dir = os.environ['WIKICHRON_DATA_DIR']

dest_path = os.path.join('precooked_data', 'networks')

def main(*args):

    if not os.path.isdir(data_dir):
        print('Error: the path "{}" was not found'.format(source_path))
        return 1

    if not os.path.isdir(dest_path):
        print(f'Creating bin directory for first time: {dest_path}')
        os.makedirs(dest_path)

    wikis = json.load(open(os.path.join(data_dir, 'wikis.json')))

    for wiki in wikis:
        df = lib.get_dataframe_from_csv(os.path.join(data_dir, wiki['data']))
        lib.prepare_data(df)
        df = lib.clean_up_bot_activity(df, wiki)

        for net in lib.get_available_networks():
            print(f"Generating network binary data for {wiki['name']}")
            time_start_generating_network = time.perf_counter()

            net.generate_from_pandas(data = df)
            time_end_generating_network = time.perf_counter() - time_start_generating_network
            print(' * [Timing] Generating network for {} : {} seconds'
                    .format(wiki['name'], time_end_generating_network))

            o_f = wiki['data'][:-3]
            o_f = '{}{}.bin'.format(o_f, net.code)
            net.write_pickle(fname = os.path.join(dest_path, o_f))

    return 0


if __name__ == '__main__':
    main()
