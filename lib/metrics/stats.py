#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   stats.py

   Descp:

   Created on: 14-nov-2017

   Copyright 2017 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

import pandas as pd

global index;

# Mandatory to run before to calculate any stats!!
# TOREDESIGN & TOIMPROVE!
def init_stats(data):
    global index;
    monthly_data = data.groupby(pd.Grouper(key='timestamp',freq='M'))
    index = monthly_data.size().index

# Pages

def pages_new(data):
    global index;
    pages = data.drop_duplicates('page_id')
    series = pages.groupby(pd.Grouper(key='timestamp',freq='M')).size()
    return series.reindex(index, fill_value=0)

def pages_accum(data):
    return (pages_new(data).cumsum())

def pages_main_new(data):
    global index;
    pages = data.drop_duplicates('page_id')
    main_pages = pages[pages['page_ns'] == 0]
    series = main_pages.groupby(pd.Grouper(key='timestamp',freq='M')).size()
    return series.reindex(index, fill_value=0)

def pages_main_accum(data):
    return (pages_main_new(data).cumsum())

def pages_edited(data):
    global index;
    monthly_data = data.groupby([pd.Grouper(key='timestamp',freq='M')])
    series = monthly_data.apply(lambda x: len(x.page_id.unique()))
    return series.reindex(index, fill_value=0)

def main_edited(data):
    global index;
    main_pages = data[data['page_ns'] == 0]
    monthly_data = main_pages.groupby([pd.Grouper(key='timestamp',freq='M')])
    series = monthly_data.apply(lambda x: len(x.page_id.unique()))
    return series.reindex(index, fill_value=0)

########################################################################

# Editions

def edits(data):
    global index;
    monthly_data = data.groupby(pd.Grouper(key='timestamp',freq='M'))
    series = monthly_data.size()
    return series.reindex(index, fill_value=0)

def edits_accum(data):
    return (edits(data).cumsum())

def edits_main_content(data):
    edits_main_data = data[data['page_ns'] == 0]
    return (edits(edits_main_data))

def edits_main_content_accum(data):
    return (edits_main_content(data).cumsum())

def edits_article_talk(data):
    edits_talk_data = data[data['page_ns'] == 1]
    return (edits(edits_talk_data))

def edits_user_talk(data):
    edits_talk_data = data[data['page_ns'] == 3]
    return (edits(edits_talk_data))

########################################################################

# Users

def users_active(data):
    global index;
    monthly_data = data.groupby(pd.Grouper(key='timestamp',freq='M'))
    series = monthly_data.apply(lambda x: len(x.contributor_id.unique()))
    return series.reindex(index, fill_value=0)

def users_new(data):
    global index;
    users = data.drop_duplicates('contributor_id')
    series = users.groupby(pd.Grouper(key='timestamp',freq='M')).size()
    return series.reindex(index, fill_value=0)

def users_accum(data):
    return (users_new(data).cumsum())

def users_new_anonymous(data):
    users = data.drop_duplicates('contributor_id')
    anonymous_users = users[users['contributor_name'] == 'Anonymous']
    series = anonymous_users.groupby(pd.Grouper(key='timestamp',freq='M')).size()
    return series.reindex(index, fill_value=0)

def users_anonymous_accum(data):
    return (users_new_anonymous(data).cumsum())

def users_new_registered(data):
    users = data.drop_duplicates('contributor_id')
    anonymous_users = users[users['contributor_name'] != 'Anonymous']
    series =  anonymous_users.groupby(pd.Grouper(key='timestamp',freq='M')).size()
    return series.reindex(index, fill_value=0)

def users_registered_accum(data):
    return (users_new_registered(data).cumsum())

########################################################################

# Combined

def edits_per_users_accum(data):
    return (edits_accum(data) / users_accum(data))

def edits_per_users_monthly(data):
    return (edits(data) / users_active(data))

def edits_per_pages_accum(data):
    return (edits_accum(data) / pages_accum(data))

def edits_per_pages_monthly(data):
    return (edits(data) / pages_edited(data))


