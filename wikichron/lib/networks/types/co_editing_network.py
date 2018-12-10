#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   co_editing_network.py

   Descp:

   Created on: 10-dic-2018

   Copyright 2018 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""
from datetime import datetime

def to_cytoscape_dict(di_net):
    """
    Transform an input dict to cytoscape network

    Parameters:
        -di_net: actual network to transform

    Return:
        A dict with the cytoscape structure of nodes and edges
    """
    network = []
    min_v = float('Inf')
    max_v = -1
    for key, val in di_net['nodes'].items():

        if min_v > val['num_edits']:
            min_v = val['num_edits']
        if max_v < val['num_edits']:
            max_v = val['num_edits']

        network.append({
            'data': {
                'id': key,
                'label': val['label'],
                'num_edits': val['num_edits'],
                'first_edit': val['first_edit'],
                'last_edit': val['last_edit']
            }
        })

    di_net['user_max_edits'] = max_v
    di_net['user_min_edits'] = min_v
    min_v = float('Inf')
    max_v = -1
    for key, val in di_net['edges'].items():

        if min_v > val['weight']:
            min_v = val['weight']
        if max_v < val['weight']:
            max_v = val['weight']

        network.append({
            'data': {
                'id': key,
                'source': val['source'],
                'target': val['target'],
                'weight': val['weight']
            }
        })

    di_net['edge_max_weight'] = max_v
    di_net['edge_min_weight'] = min_v
    di_net['nodes'] = None
    di_net['edges'] = None
    di_net['network'] = network

    # print('aristas : {}\nnodos: {}'.format(len(di_edges), len(di_nodes)))
    return di_net


def generate_network(dataframe, time_limit = datetime.now()):
    """
    Generates a dict with the network

    Parameters:
        -dataframe: A pandas object with the wiki info
        -time_limit: A datetime object, default; Actual time

    Return: A dict {nodes, edges, oldest_user, newest_user} with the network
                representation.
    """
    di_nodes = {}
    di_edges = {}
    user_per_page = {}
    oldest_user = False
    newest_user = False

    for index, r in dataframe.iterrows():
        t = (time_limit - r['timestamp'].to_pydatetime()).total_seconds()
        if t < 0:
            break

        if r['contributor_name'] == 'Anonymous':
            continue

        if not oldest_user:
            oldest_user = t

        newest_user = t
        # Nodes
        if not r['contributor_id'] in di_nodes:
            di_nodes[r['contributor_id']] = {}
            di_nodes[r['contributor_id']]['label'] = \
                                    r['contributor_name']
            di_nodes[r['contributor_id']]['num_edits'] = 0
            di_nodes[r['contributor_id']]['first_edit'] = t

        di_nodes[r['contributor_id']]['num_edits'] += 1
        di_nodes[r['contributor_id']]['last_edit'] = r['timestamp']

        # A page gets serveral contributors
        if not r['page_id'] in user_per_page:
            user_per_page[r['page_id']] = {r['contributor_id']}
        else:
            user_per_page[r['page_id']].add(r['contributor_id'])

    # Edges
    for k, p in user_per_page.items():
        aux = list(p)
        for i in range(len(aux)):
            for j in range(i+1, len(aux)):
                key1 = '{}{}'.format(aux[i],aux[j])
                key2 = '{}{}'.format(aux[j],aux[i])
                if key1 in di_edges:
                    di_edges[key1]['weight'] += 1
                    continue
                if key2 in di_edges:
                    di_edges[key2]['weight'] += 1
                    continue
                di_edges[key1] = {}
                di_edges[key1]['source'] = aux[i]
                di_edges[key1]['target'] = aux[j]
                di_edges[key1]['weight'] = 1

    return {
        'nodes': di_nodes,
        'edges': di_edges,
        'oldest_user': oldest_user,
        'newest_user': newest_user
    }



def main():
   return 0

if __name__ == '__main__':
   main()

