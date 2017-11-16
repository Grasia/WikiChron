#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   stats.py

   Descp:

   Created on: 14-nov-2017

   Copyright 2017 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

import pandas as pd

# Editions

def edits_monthly(data):
   monthly_data = data.groupby(pd.Grouper(key='timestamp',freq='M'))
   return (monthly_data.page_id.count())

# Users

def users_new(data):
  monthly_users = data.drop_duplicates('contributor_id')
  return monthly_users.groupby(pd.Grouper(key='timestamp',freq='M')).contributor_id.count()

