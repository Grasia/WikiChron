#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   is_wikia_wiki.py

   Descp: A very simple aux module to re-use code to determine if an url is
        own by Fandom / Wikia or not.

   Created on: 06-jun-2019

   Copyright 2019 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

import re


def is_wikia_wiki(url):
    return (re.search('.*\.(fandom|wikia)\.(com|org).*', url) != None)
