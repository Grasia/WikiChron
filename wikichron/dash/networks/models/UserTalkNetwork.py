"""
   UserTalkNetwork.py

   Descp: Implementation of User-Talk Pages

   Created on: 16/03/2019

   Copyright 2019 Youssef 'FRYoussef' El Faqir el Rhazoui <f.r.youssef@hotmail.com>
"""

import pandas as pd
import re

from .BaseNetwork import BaseNetwork

class UserTalkNetwork(BaseNetwork):
    """
    This class use user-talk pages to perform a network,
    where NODES are wiki users who edit in a user-talk page, and a tie
    is inferred when user A edits the B's user-talk-page.
    Thus the EDGES are directed.

    Arguments:
        - Node:
            * num_edits: the number of edits in itself's user-talk-page
            * article_edits: edits in article pages
            * talk_edits: edits in talk pages
            * id: The user id in the wiki
            * label: the user name in the wiki

        - Edge:
            * id: sourceId + targetId
            * source: user_id
            * target: user_id
            * weight: the number of editions in the user-talk-page
    """

    NAME = 'User Talk Pages'
    CODE = 'user_talk_network'
    DIRECTED = True

    AVAILABLE_METRICS = {
        'Edits in its own page': 'num_edits',
        'Betweenness': 'betweenness',
        'Page Rank': 'page_rank'
    }

    SECONDARY_METRICS = {
        'Absolute Longevity': {
            'key': 'abs_birth_int',
            'max': 'max_abs_birth_int',
            'min': 'min_abs_birth_int'
        },
        'Article Edits': {
            'key': 'article_edits',
            'max': 'max_article_edits',
            'min': 'min_article_edits'
        },
        'Talk Edits': {
            'key': 'talk_edits',
            'max': 'max_talk_edits',
            'min': 'min_talk_edits'
        }
    }

    USER_INFO = {
        'User ID': 'id',
        'User Name': 'label',
        'Absolute Birth': 'abs_birth',
        'Cluster': 'cluster',
        'Article Edits': 'article_edits',
        'Talk Page Edits': 'talk_edits'
    }

    def __init__(self, is_directed = True, graph = {}):
        super().__init__(is_directed = is_directed, graph = graph)


    def generate_from_pandas(self, df):
        user_per_page = {}
        mapper_v = {}
        count_v = 0
        count_e = 0

        dff = self.remove_non_user_talk_data(df)
        for _, r in dff.iterrows():
            # Nodes
            if not r['contributor_name'] in mapper_v:
                self.graph.add_vertex(count_v)
                mapper_v[r['contributor_name']] = count_v
                self.graph.vs[count_v]['id'] = int(r['contributor_id'])
                self.graph.vs[count_v]['label'] = r['contributor_name']
                self.graph.vs[count_v]['num_edits'] = 0
                count_v += 1

            page_t = re.sub('^.+:', '', r['page_title'])
            # remove everyhing after slash
            page_t = re.sub('[\/].*', '', page_t)
            # filter anonymous user talk page for ipv4 or ipv6 (i.e it contains "." or ":")
            if re.search('\.|\:', page_t):
                continue # We skip anonymous

            if page_t == r['contributor_name']:
                self.graph.vs[mapper_v[page_t]]['num_edits'] += 1
            else:
                # A page gets serveral contributors
                if not page_t in user_per_page:
                    user_per_page[page_t] = {r['contributor_name']: 1}
                else:
                    if r['contributor_name'] in user_per_page[page_t]:
                        user_per_page[page_t][r['contributor_name']] += 1
                    else:
                        user_per_page[page_t][r['contributor_name']] = 1

        # Edges
        if self.graph.vcount():
            max_id = max(self.graph.vs['id']) + 1
        else:
            max_id = 1

        for page_name, p_dict in user_per_page.items():
            for user, edits in p_dict.items():
                # it could be that an user has no edits but someone edits in its user-talk
                if page_name not in mapper_v:
                    self.graph.add_vertex(count_v)
                    mapper_v[page_name] = count_v
                    self.graph.vs[count_v]['id'] = max_id
                    max_id += 1
                    self.graph.vs[count_v]['label'] = page_name
                    self.graph.vs[count_v]['num_edits'] = 0
                    count_v += 1

                self.graph.add_edge(mapper_v[user], mapper_v[page_name])
                source = self.graph.vs[mapper_v[user]]['id']
                target = self.graph.vs[mapper_v[page_name]]['id']
                edge_id = (source << 32) + target
                self.graph.es[count_e]['id'] = edge_id
                self.graph.es[count_e]['weight'] = edits
                self.graph.es[count_e]['source'] = source
                self.graph.es[count_e]['target'] = target
                count_e += 1


    def get_metric_dataframe(self, metric):
        if self.AVAILABLE_METRICS[metric] in self.graph.vs.attributes()\
            and 'label' in self.graph.vs.attributes():

            df = pd.DataFrame({
                    'User': self.graph.vs['label'],
                    metric: self.graph.vs[self.AVAILABLE_METRICS[metric]]
                    })
            return df

        return pd.DataFrame()


    @classmethod
    def get_available_metrics(cls) -> dict:
        return cls.AVAILABLE_METRICS


    @classmethod
    def get_user_info(cls) -> dict:
        return cls.USER_INFO


    @classmethod
    def get_secondary_metrics(cls) -> dict:
        return cls.SECONDARY_METRICS


    def add_graph_attrs(self):
        super().add_graph_attrs()
        for _, val in self.SECONDARY_METRICS.items():
            if val['key'] in self.graph.vs.attributes():
                self.graph[val['max']] = max(self.graph.vs[val['key']])
                self.graph[val['min']] = min(self.graph.vs[val['key']])


    @classmethod
    def is_directed(cls):
        return cls.DIRECTED


    def add_others(self, df):
        self.calculate_edits(df, 'article')
        self.calculate_edits(df, 'talk')
