#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   generate_wiki_network.py

   Descp: This script generates a network per wiki csv. It get them from ../data
    and creates a bin|gml network in precooked_data/networks

    Parameters: 
        -bin or nothing: to write a bin network
        -gml: to write a gml network

   Created on: 17-dic-2018

   Copyright 2018 Youssef El Faqir El Rhazoui <f.r.youssef@hotmail.com>
   Copyright 2018 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>

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

def main(*args):
    if len(sys.argv) > 2:
        print('Error: Invalid number of arguments')
        return 1

    write_bin = True
    dest_path = os.path.join('precooked_data', 'networks')
    if len(sys.argv) == 2:
        if sys.argv[1] == '-gml':
            write_bin = False
            dest_path = os.path.join(dest_path, 'gml')
        elif sys.argv[1] == '-bin':
            write_bin = True
            dest_path = os.path.join(dest_path, 'bin')
        else:
            print(f'Error: argument {sys.argv[1]} is not allowed')
            return 1

    if not os.path.isdir(data_dir):
        print('Error: the path "{}" was not found'.format(source_path))
        return 1

    if not os.path.isdir(dest_path):
        print(f'Creating directory for first time: {dest_path}')
        os.makedirs(dest_path)

    wikis = json.load(open(os.path.join(data_dir, 'wikis.json')))

    for wiki in wikis:
        df = lib.get_dataframe_from_csv(os.path.join(data_dir, wiki['data']))
        lib.prepare_data(df)
        df = lib.clean_up_bot_activity(df, wiki)

        net = CoEditingNetwork()
        print(f"Generating network data for {wiki['name']}")
        time_start_generating_network = time.perf_counter()

        net.generate_from_pandas(data = df)
        time_end_generating_network = time.perf_counter() - time_start_generating_network
        print(' * [Timing] Generating network for {} : {} seconds'
                .format(wiki['name'], time_end_generating_network))
        o_f = wiki['data'][:-3]
        if write_bin:
            o_f = '{}{}.bin'.format(o_f, net.code)
            net.write_pickle(fname = os.path.join(dest_path, o_f))
        else:
            o_f = '{}{}.gml'.format(o_f, net.code)
            net.write(f=os.path.join(dest_path, o_f), format='gml')


    return 0


if __name__ == '__main__':
    sys.exit(main())
