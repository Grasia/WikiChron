#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
   data_manager.py

   Descp: Auxiliar python module with common functions related to load and
       management of data and metadata for the whole flask application.

   Created on: 27-may-2019

   Copyright 2019 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

import pandas as pd
import csv
import json
import os
import zc.lockfile

data_dir = os.getenv('WIKICHRON_DATA_DIR', 'data')


def get_available_wikis():
    wikis_json_file = open(os.path.join(data_dir, 'wikis.json'))
    wikis = json.load(wikis_json_file)
    return wikis


def get_max_wiki_stats():
    wikis = get_available_wikis()
    max_stats = {}
    max_stats['edits'] = []

    return max_stats


def update_wikis_metadata(new_metadata):
    # if file is not locked, open it and lock it
    try:
        filename = os.path.join(data_dir, 'wikis.json')
        lock = zc.lockfile.LockFile(filename)
        wikis_json_file = open(filename, 'w')
    except:
        return False

    # update file with new metadata and release file
    try:
        json.dump(new_metadata, wikis_json_file, indent='\t')
        return True
    except:
        return False
    finally:
        # release lock if got it
        wikis_json_file.close()
        lock.close()


def load_dataframe_from_csv(csv: str):
    df = pd.read_csv(os.path.join(data_dir, csv),
                    delimiter=',', quotechar='|',
                    index_col=False)
    df['timestamp']=pd.to_datetime(df['timestamp'],format='%Y-%m-%dT%H:%M:%SZ')
    return df


def get_stats(data : pd.DataFrame) -> dict:
    stats = {}

    stats['edits'] = data['revision_id'].nunique()
    stats['pages'] = data['page_id'].nunique()
    stats['users'] = data['contributor_id'].nunique()
    stats['articles'] = data[data['page_ns'] == 0]['page_id'].nunique()

    data = data.sort_values(by = 'timestamp')
    first_edit = data.head(1)
    stats['first_edit'] = {
                    'revision_id': int(first_edit['revision_id'].values[0]),
                    'date': str(first_edit['timestamp'].values[0])
                    }

    last_edit = data.tail(1)
    stats['last_edit'] = {
                    'revision_id': int(last_edit['revision_id'].values[0]),
                    'date': str(last_edit['timestamp'].values[0])
                    }

    return stats

