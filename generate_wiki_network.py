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
from wikichron.lib.networks.types.CoEditingNetwork import CoEditingNetwork

def main(*args):
	source_path = os.path.join('.', 'data')

	if not os.path.isdir(source_path):
		print('Error: the path "{}" was not found'.format(source_path))
		return 1

	dest_path = os.path.join('.', 'precooked_data', 'networks')
	row = pd.read_csv(os.path.join(source_path, 'wikis.csv'), 
					delimiter=', ', quotechar='|', index_col=False)

	for i, f in row.iterrows():
		df = lib.get_dataframe_from_csv(f['csvfile'])
		lib.prepare_data(df)
		df = lib.clean_up_bot_activity(df, f['csvfile'])
		for net in lib.get_available_networks():
			net.generate_from_pandas(data=df)
			o_f = f['csvfile'][:-3]
			o_f = '{}{}.bin'.format(o_f, net.code)
			net.write_pickle(fname=os.path.join(dest_path, o_f))
	
	return 0


if __name__ == '__main__':
    sys.exit(main())