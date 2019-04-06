#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   get_wikia_images_base64.py

   Descp: Get wikia images, when existent, and transform them to base64.
      It needs an input file with the wikis to be added.
      That file has to have the wikis urls and their corresponding csv data
      filename.

   Created on: 14-mar-2019

   Copyright 2019 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

import csv
import requests
import json
import os
import re
import base64
import shutil
from bs4 import BeautifulSoup


if 'WIKICHRON_DATA_DIR' in os.environ:
    data_dir = os.environ['WIKICHRON_DATA_DIR']
else:
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')

input_wikis_fn = os.path.join(data_dir, 'wikis.csv')


def get_wikia_wordmark_api(domain): # doesn't work properly :(
    wikia_api_endpoint = 'http://www.wikia.com/api/v1/Wikis/ByString?expand=1&limit=25&batch=1&includeDomain=true&string='

    res = requests.get(wikia_api_endpoint + domain)
    status_code = res.status_code
    if status_code == 200:
        json_res = json.loads(res.text)
        if (len(json_res['items']) >= 1):
            wikis = json_res['items']
            wiki_info = None
            for wiki in wikis:
                if wiki['domain'] == domain:
                    wiki_info = wiki
                    break;

            if wiki_info and wiki_info['wordmark']:
                    img_url = wiki_info['wordmark']
                    img_res = requests.get(img_url, stream=True)
                    status_code = img_res.status_code
                    if status_code == 200:
                        b64 = base64.encodebytes(img_res.content)
                        return '"data:image/png;base64,{}"'.format(str(b64, encoding='utf-8'))

    else:
        print (status_code)

    return None


def get_wikia_wordmark_file(domain):
    url = 'https://' + domain + '/wiki/File:Wiki-wordmark.png'
    res = requests.get(url)
    status_code = res.status_code
    if status_code == 200:

        # Process HTML with bs4 to find img src="" value
        html = BeautifulSoup(res.text,"lxml")
        img = html.select_one('#file img')
        if not img:
            return None

        img_url = img.attrs['data-src']

        img_res = requests.get(img_url, stream=True)
        status_code = img_res.status_code
        if status_code == 200:
            b64 = base64.b64encode(img_res.content)
            return 'data:image/png;base64,{}'.format(str(b64, encoding='utf-8'))

    else:
        print (status_code)
        return None


def is_wikia_wiki(url):
    return (re.search('.*\.(fandom|wikia)\.com.*', url) != None)


def main():
    wikisfile = open(input_wikis_fn, newline='')
    wikisreader = csv.DictReader(wikisfile, skipinitialspace=True)

    for row in wikisreader:
        print(row['url'], row['csvfile'])

        b64 = None
        if (is_wikia_wiki(row['url'])):
            b64 = get_wikia_wordmark_file(row['url'])

        if b64:
            print(b64)
        else:
            print('')

        print('-------------------\n')

    wikisfile.close()

    return 0


if __name__ == '__main__':
   main()
