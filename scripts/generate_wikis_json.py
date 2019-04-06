#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   generate_wikis_json.py

   Descp: Generate a wikis.json suitable for Wikichron.
      It needs an input file with the wikis to be added.
      That file has to have the wikis urls and their corresponding csv data
      filename.

   Created on: 09-mar-2018

   Copyright 2018-2019 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

import csv
import requests
from bs4 import BeautifulSoup
import json
import os
import re
import pandas as pd
from datetime import date

from query_bot_users import get_bots
from get_wikia_images_base64 import get_wikia_wordmark_file

if 'WIKICHRON_DATA_DIR' in os.environ:
    data_dir = os.environ['WIKICHRON_DATA_DIR']
else:
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')

input_wikis_fn = os.path.join(data_dir, 'wikis.csv')
output_wikis_fn = os.path.join(data_dir, 'wikis.json')
row_selector = "tr.mw-statistics-"
stats = ['articles','pages','edits']


def get_name(base_url):

    url = 'https://' + base_url

    req = requests.get(url)
    if req.status_code != 200:
        print (req.status_code)
        req.raise_for_status()
        return 'Unknown'

    try:
        # Process HTML with bs4
        html = BeautifulSoup(req.text,"lxml")
        name = html.select_one('div.wds-community-header__sitename a').text
    except AttributeError:
        print('Name could not be retrieved from html.')
        return 'Unknown'

    return name


def is_wikia_wiki(url):
    return (re.search('.*\.(fandom|wikia)\.com.*', url) != None)


def get_stats(data : pd.DataFrame) -> dict:
    stats = {}

    stats['edits'] = data['revision_id'].nunique()
    stats['pages'] = data['page_id'].nunique()
    stats['users'] = data['contributor_id'].nunique()
    stats['articles'] = data[data['page_ns'] == 0]['page_id'].nunique()

    data = data.sort_values(by = 'timestamp')
    first_edit = data.head(1)
    stats['first_edit'] = {
                    'revision_id': int(first_edit['revision_id'].values[0]),
                    'date': str(first_edit['timestamp'].values[0])
                    }

    last_edit = data.tail(1)
    stats['last_edit'] = {
                    'revision_id': int(last_edit['revision_id'].values[0]),
                    'date': str(last_edit['timestamp'].values[0])
                    }

    return stats


def load_dataframe_from_csv(csv: str):
    df = pd.read_csv(os.path.join(data_dir, csv),
                    delimiter=',', quotechar='|',
                    index_col=False)
    df['timestamp']=pd.to_datetime(df['timestamp'],format='%Y-%m-%dT%H:%M:%SZ')
    return df


def main():
    wikisfile = open(input_wikis_fn, newline='')
    wikisreader = csv.DictReader(wikisfile, skipinitialspace=True)

    wikis = []

    for row in wikisreader:
        print(row['url'], row['csvfile'])
        wiki = {}
        wiki['url'] = row['url']
        wiki['data'] = row['csvfile']

        wiki_df = load_dataframe_from_csv(wiki['data'])
        result_stats = get_stats(wiki_df)

        if result_stats:
            wiki.update(result_stats)
        else:
            raise Exception(f'Wiki {wiki["url"]} is not reacheable. Possibly moved or deleted. Check, whether its url is correct.')

        wiki['bots'] = get_bots(wiki['url'])


        wiki['lastUpdated'] = str(date.today())

        wiki['verified'] = True # Our own provided wikis are "verified"

        print(wiki)

        wikis.append(wiki)

    wikisfile.close()

    result_json = json.dumps(wikis)
    print(result_json)

    try:
        output_wikis = open(output_wikis_fn)
        wikis_json = json.load(output_wikis)
        current_wikis_positions = { wiki['url']:pos for (pos, wiki) in enumerate(wikis_json) }
        print(f'\nWe already had these wikis: {list(current_wikis_positions.keys())}')
        output_wikis.close()
    except FileNotFoundError:
        current_wikis_positions = {}
        wikis_json = []

    for wiki in wikis:
        if wiki['url'] in current_wikis_positions: # already in wikis.json
            position = current_wikis_positions[wiki['url']]
            wikis_json[position].update(wiki)
        else:                                      # new wiki for wikis.json
            # get name and image only for new wiki entries
            wiki['name'] = get_name(wiki['url'])
            if (is_wikia_wiki(wiki['url'])):
                b64 = get_wikia_wordmark_file(wiki['url'])
                if b64:
                    wiki['imageSrc'] = b64
                else:
                    print(f'\n-->Failed to find image for wiki: {wiki["url"]}<--\n')
            # append to wikis.json
            wikis_json.append(wiki)

    output_wikis = open(output_wikis_fn, 'w')
    json.dump(wikis_json, output_wikis, indent='\t')
    output_wikis.close()

    print(f'\nWikis updated: {[wiki["url"] for wiki in wikis]}')

    return 0


if __name__ == '__main__':
   main()
