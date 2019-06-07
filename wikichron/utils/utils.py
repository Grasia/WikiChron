#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
   utils.py

   Descp: Python module with auxiliar functions.

   Created on: 06-jun-2019

   Copyright 2019 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

import re


def get_domain_from_url(url):
    domain = re.match('https?://(.*)', url)
    return domain.groups()[0]
