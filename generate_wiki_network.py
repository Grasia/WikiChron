"""
    This script generates a network per wiki csv. It get them from ../data
    and creates a bin network in precooked_data/networks
"""
#
# Author: Youssef El Faqir El Rhazoui
# Date: 07/12/2018
# Distributed under the terms of the GPLv3 license.
#

import os
from os.path import join
import sys
import wikichron.lib.interface as lib
import pandas as pd
import json
import time

from wikichron.lib.networks.types.CoEditingNetwork import CoEditingNetwork

source_path = os.path.join('.', 'data')
dest_path = os.path.join('.', 'precooked_data', 'networks')

def main(*args):

    if not os.path.isdir(source_path):
        print('Error: the path "{}" was not found'.format(source_path))
        return 1


    if not os.path.isdir(dest_path):
        print(f'Creating bin directory for first time: {dest_path}')
        print(dest_path)
        os.makedirs(dest_path)


    wikis = json.load(open(os.path.join(lib.data_dir, 'wikis.json')))

    for wiki in wikis:
        df = lib.get_dataframe_from_csv(wiki['data'])
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
        sys.exit(0)

    return 0


if __name__ == '__main__':
    main()
