#!/usr/bin/env python3
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
import base64
import shutil
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from is_wikia_wiki import is_wikia_wiki


if 'WIKICHRON_DATA_DIR' in os.environ:
    data_dir = os.environ['WIKICHRON_DATA_DIR']
else:
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')

input_wikis_fn = os.path.join(data_dir, 'wikis.csv')


def get_wikia_wordmark_api(domain):
    wikia_api_endpoint = 'http://community.fandom.com/api/v1/Wikis/ByString?expand=1&limit=25&batch=1&includeDomain=true&string='

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

            if wiki_info and wiki_info['image']:
                    img_url = wiki_info['image']
                    img_res = requests.get(img_url, stream=True)
                    status_code = img_res.status_code
                    if status_code == 200:
                        b64 = base64.encodebytes(img_res.content)
                        return '"data:image/png;base64,{}"'.format(str(b64, encoding='utf-8'))

    else:
        print (status_code)

    return None


def get_wikia_wordmark_file(url): # needs to be updated
    url = url + '/wiki/File:Wiki-wordmark.png'
    res = requests.get(url)
    status_code = res.status_code
    if status_code == 200:

        # Process HTML with bs4 to find img src="" value
        html = BeautifulSoup(res.text,"lxml")
        img_link = html.select_one('.see-full-size-link')

        print(img_link)

        if not img_link:
            return None

        img_url = img_link.href

        print(img_url)

        img_res = requests.get(img_url, stream=True)
        status_code = img_res.status_code
        if status_code == 200:
            b64 = base64.b64encode(img_res.content)
            return 'data:image/png;base64,{}'.format(str(b64, encoding='utf-8'))

    else:
        print (status_code)
        return None


def main():
    wikisfile = open(input_wikis_fn, newline='')
    wikisreader = csv.DictReader(wikisfile, skipinitialspace=True)

    for row in wikisreader:
        print(row['url'], row['csvfile'])

        b64 = None
        # using API
        if (is_wikia_wiki(row['url'])):
            domain = urlparse(row['url']).netloc
            b64 = get_wikia_wordmark_api(domain)

        if b64:
            print(b64)
        else:
            print('')

        # using special:file
        if (is_wikia_wiki(row['url'])):
            b64 = get_wikia_wordmark_file(row['url'])


        print('-------------------\n')

    wikisfile.close()

    return 0


if __name__ == '__main__':
   main()
