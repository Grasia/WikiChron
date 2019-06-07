#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
   query_bot_users.py

   Descp: A simple script to download the bot users of a certain wiki
   and output the user ids in an output file readable for pandas.
   It uses the mediawiki endpoint api.php to do the queries.

   Created on: 09-feb-2018

   Copyright 2018 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

import requests
import sys
import json
import re

from is_wikia_wiki import is_wikia_wiki


wikia_api_endpoint = 'api.php?action=query&list=groupmembers&gmgroups=bot|bot-global&gmlimit=500&format=json'
mediawiki_api_endpoint = 'api.php?action=query&list=allusers&augroup=bot&aulimit=500&auprop=groups&format=json'

def mediawiki_get_bots(base_url):
   """
   Query the mediwiki api enpoint for standard mediawiki wikis
    and returns a list of bot dictionaries, where each one of them
    has this structure: {botid: botname}
   """
   def api_probing(base_url):

      if base_url[-1:] != '/':
         base_url += ('/')

      url = base_url + 'w/' + mediawiki_api_endpoint
      if (requests.get(url)):
         return url

      url = base_url + 'wiki/' + mediawiki_api_endpoint
      if (requests.get(url)):
         return url

      url = base_url + mediawiki_api_endpoint
      if (requests.get(url)):
         return url

      return None


   url = api_probing(base_url)
   if not url:
      raise Exception('Not wiki endpoint found in this url: {}'.format(base_url))
   print('Making request to: {}'.format(url))
   continue_query = True
   bots = []
   while (continue_query):
      r = requests.get(url)
      res = r.json()
      print(res)
      for bot in res['query']['allusers']:
         botid = str(bot['userid'])
         botname = str(bot['name'])
         bots.append( {"id": botid, "name": botname} )
      continue_query = 'continue' in res
      if (continue_query):
         url += '&aufrom=' + res['continue']['aufrom']

   return bots


def wikia_get_bots(base_url, offset=0):
   """
   Query the mediawiki enpoint for Wikia wikis and returns a list of bot userids
   """
   if base_url[:-1] != '/':
      base_url += ('/')
   url = base_url + wikia_api_endpoint + '&gmoffset={}'.format(offset)
   #~ print(url)
   r = requests.get(url)
   res = r.json()
   bots = []
   for bot in res['users']:
      botid = str(bot['userid'])
      botname = str(bot['name'])
      bots.append( {"id": botid, "name": botname} )
   if 'query-continue' in res:
      return bots + get_bots_ids(base_url, offset=res['query-continue']['groupmembers']['gmoffset'])
   else:
      return bots


def write_outputfile(filename, bots):
   import numpy as np
   np.array(bots).tofile(filename, sep=',')


def get_bots(url):
   if is_wikia_wiki(url): # detect Wikia wikis
      return wikia_get_bots(url)
   else:
      return mediawiki_get_bots(url)


def main():
   help = """This script gives you the bot user ids for a given set of wikis.\n
            Syntax: python3 query_bot_users url1 [url2, url3,...]""";

   if(len(sys.argv)) >= 2:
      if sys.argv[1] == 'help':
         print(help);
         exit(0)

      for url in sys.argv[1:]:
         if not (re.search('^http', url)):
            url = 'http://' + url
         print("Retrieving data for: " + url)
         bots = get_bots(url)

         print("These are the bots ids:")
         print(json.dumps(bots))
         print("<" + "="*50 + ">")
   else:
      print("Error: Invalid number of arguments. Please specify one or more wiki urls to get the bots from.", file=sys.stderr)
      print(help)
      exit(1)

if __name__ == '__main__':
   main()



