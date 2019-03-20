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


def get_nonbot_users_no(url):
    """
    Get actual number of nonbots users of a wiki.
    It makes two requests to the Special:ListUsers endpoint.
    One for all users and one for bots users, and it substracts all users number
    by bot users number.
    """

    def query_users(url, only_bots):
        """
        Make a POST request to the Special:ListUsers endpoint
        It can query for all users of the wiki (including bots)
        of for bots users only.
        """

        if not only_bots:
            data = {
                'groups': "all,bot,bureaucrat,rollback,sysop,threadmoderator,authenticated,bot-global,content-reviewer,content-volunteer,council,fandom-editor,global-discussions-moderator,helper,restricted-login,restricted-login-exempt,reviewer,staff,util,vanguard,voldev,vstf,",
                'username': "",
                'edits': 0,
                'limit': "50",
                'offset': "0",
                'loop': 0 # simulate user behaviour
            }
        else:
            data = {
                'groups': "bot,bot-global,",
                'username': "",
                'edits': 0,
                'limit': "50",
                'offset': "0",
                'loop': 1 # simulate user behaviour
            }

        req = requests.post(url, data)

        # Checking status code before returning count number
        if 200 == req.status_code:
            return req.json()['iTotalDisplayRecords']
        else:
            req.raise_for_status()


    users_url = url + '/index.php?action=ajax&rs=ListusersAjax::axShowUsers'
    return query_users(users_url, False) - query_users(users_url, True)


def is_wikia_wiki(url):
    return (re.search('.*\.(fandom|wikia)\.com.*', url) != None)


def main():
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
        wiki['bots'] = get_bots(url)

        result_stats = get_stats(url)
        wiki.update(result_stats)

        users_no = get_nonbot_users_no(url)
        wiki['users'] = users_no

        if (is_wikia_wiki(wiki['url'])):
            b64 = get_wikia_wordmark_file(wiki['url'])
            if b64:
                wiki['imageSrc'] = b64
            else:
                print(f'\n-->Failed to find image for wiki: {wiki["url"]}<--\n')

        print(wiki)

        wikis.append(wiki)

        #~ print(', '.join(row))

    wikisfile.close()

    #~ result_json = json.dumps(wikis)
    #~ print(result_json)

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
        if wiki['url'] in current_wikis_positions:
            position = current_wikis_positions[wiki['url']]
            wikis_json[position].update(wiki)
        else:
            wikis_json.append(wiki)
    output_wikis = open(output_wikis_fn, 'w')
    json.dump(wikis_json, output_wikis, indent='\t')
    output_wikis.close()

    print(f'\nWikis updated: {[wiki["url"] for wiki in wikis]}')

    return 0


if __name__ == '__main__':
   main()
