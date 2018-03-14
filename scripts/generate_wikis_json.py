#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   generate_wikis_json.py

   Descp: Generate a wikis.json suitable for Wikichron.
      It needs an input file with the wikis to be added.
      That file has to have the wikis urls and their corresponding csv data
      filename.

   Created on: 09-mar-2018

   Copyright 2018 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

import csv
import requests
from bs4 import BeautifulSoup
import json
import os

from query_bot_users import get_bots_ids

if 'WIKICHRON_DATA_DIR' in os.environ:
   data_dir = os.environ['WIKICHRON_DATA_DIR']
else:
   data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')

input_wikis_fn = os.path.join(data_dir, 'wikis.csv')
output_wikis_fn = os.path.join(data_dir, 'wikis.json')
row_selector = "tr.mw-statistics-"
stats = ['articles','pages','edits','users']


def get_name(url):
   req = requests.get(url)
   if req.status_code != 200:
      print (req.status_code)
      req.raise_for_status()


def get_stats(base_url):

   url = base_url + "/wiki/Special:Statistics"

   # HTTP request to the web
   req = requests.get(url)

   if req.status_code != 200:
      print (req.status_code)
      return False

   # Process HTML with bs4
   html = BeautifulSoup(req.text,"lxml")
   name = html.select_one('div.wds-community-header__sitename a').text

   result = {}
   result['name'] = name
   for stat in stats:
      row = html.select_one(row_selector+stat+" td.mw-statistics-numbers")
      text = row.text.replace(',','')
      text = text.replace('.','')
      text = text.replace('\xa0', '')
      value = int(text)
      result[stat] = value

   return result


wikisfile = open(input_wikis_fn, newline='')
wikisreader = csv.DictReader(wikisfile, skipinitialspace=True)

wikis = []

for row in wikisreader:
   print(row['url'], row['csvfile'])
   wiki = {}
   wiki['url'] = row['url']
   wiki['data'] = row['csvfile']

   url = 'http://' + wiki['url']
   #~ wiki.name = get_name(url)
   wiki['botsids'] = get_bots_ids(url)

   result_stats = get_stats(url)
   wiki.update(result_stats)

   print(wiki)

   wikis.append(wiki)

   #~ print(', '.join(row))

wikisfile.close()

#~ result_json = json.dumps(wikis)
#~ print(result_json)

try:
   output_wikis = open(output_wikis_fn)
   wikis_json = json.load(output_wikis)
   print(wikis_json)
   output_wikis.close()
except:
   wikis_json = []

for wiki in wikis:
   if wiki not in wikis_json:
      wikis_json.append(wiki)
output_wikis = open(output_wikis_fn, 'w')
json.dump(wikis_json, output_wikis, indent='\t')
output_wikis.close()

#~ def main():
   #~ return 0

#~ if __name__ == '__main__':
   #~ main()

