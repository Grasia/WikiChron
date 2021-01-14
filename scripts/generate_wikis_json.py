#!/usr/bin/env python3
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
import pandas as pd
from datetime import date
import sys

from query_bot_users import get_bots
from get_wikia_images_base64 import get_wikia_wordmark_file, get_wikia_wordmark_api
from is_wikia_wiki import is_wikia_wiki

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../wikichron'))
from utils.data_manager import update_wikis_metadata, get_stats
from utils.utils import get_domain_from_url

if 'WIKICHRON_DATA_DIR' in os.environ:
    data_dir = os.environ['WIKICHRON_DATA_DIR']
else:
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')

input_wikis_fn = os.path.join(data_dir, 'wikis.csv')
output_wikis_fn = os.path.join(data_dir, 'wikis.json')
row_selector = "tr.mw-statistics-"
stats = ['articles','pages','edits']


def get_name(url):

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
        print(f'Name for wiki: {url} could not be retrieved from html.')
        return 'Unknown'

    return name


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
        wiki['domain'] = get_domain_from_url(row['url'])
        wiki['url'] = row['url']
        wiki['data'] = row['csvfile']

        wiki_df = load_dataframe_from_csv(wiki['data'])
        result_stats = get_stats(wiki_df)

        if result_stats:
            wiki.update(result_stats)
        else:
            raise Exception(f'Unable to get stats for wiki: {wiki["domain"]}.')

        try:
            print(f'Getting bots info for wiki with url: {wiki["url"]}')
            wiki['bots'] = get_bots(wiki['url'])
        except:
            print(f'Unable to get bots for wiki: {wiki["url"]}')

        wiki['lastUpdated'] = row['lastUpdated']

        wiki['verified'] = True # Wikis provided by us are "verified"
        wiki['uploadedBy'] = 'script' # How the wiki was added

        print(wiki)

        wikis.append(wiki)

    wikisfile.close()

    result_json = json.dumps(wikis)
    print(result_json)

    try:
        output_wikis = open(output_wikis_fn)
        wikis_json = json.load(output_wikis)
        current_wikis_positions = { wiki['domain']:pos for (pos, wiki) in enumerate(wikis_json) }
        print(f'\nWe already had these wikis: {list(current_wikis_positions.keys())}')
        output_wikis.close()
    except FileNotFoundError:
        current_wikis_positions = {}
        wikis_json = []

    for wiki in wikis:
        if wiki['domain'] in current_wikis_positions: # already in wikis.json
            position = current_wikis_positions[wiki['domain']]
            wikis_json[position].update(wiki)
        else:                                      # new wiki for wikis.json
            # get name and image only for new wiki entries
            wiki['name'] = get_name(wiki['url'])
            if (is_wikia_wiki(wiki['url'])):
                print(f"Getting image for wiki with url: {wiki['url']}...", end = '')
                b64 = get_wikia_wordmark_file(wiki['url'])

                if not b64:
                    print('[[Retrying using different approach]]', end = '')
                    b64 = get_wikia_wordmark_api(wiki['domain'])

                if b64:
                    wiki['imageSrc'] = b64
                    print('Success!')
                else:
                    print(f'\n-->Failed to find image for wiki: {wiki["url"]}<--\n')

            # append to wikis.json
            wikis_json.append(wiki)

    update_wikis_metadata(wikis_json)

    print(f'\nWikis updated: {[wiki["domain"] for wiki in wikis]}')

    return 0


if __name__ == '__main__':
   main()
