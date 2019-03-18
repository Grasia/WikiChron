"""
   TalkPagesNetwork.py

   Descp: Implementation of Talk Pages

   Created on: 15/03/2019

   Copyright 2019 Youssef 'FRYoussef' El Faqir el Rhazoui <f.r.youssef@hotmail.com>
"""

import pandas as pd

from .BaseNetwork import BaseNetwork


class TalkPagesNetwork(BaseNetwork):
    """
    This class use talk page to perform a network, 
    where NODES are wiki users who edit a talk page, and a tie between 
    user A and user B is inferred when they edit the same talk page.
    Thus the EDGES are undirected.

    Arguments:
        - Node:
            * num_edits: The editions number in all talk pages
            * article_edits: edits in article pages
            * id: The user id in the wiki
            * label: the user name in the wiki
        
        - Edge:
            * id: sourceId + targetId 
            * source: user_id
            * target: user_id
            * weight: the number of cooperations
    """

    NAME = 'Talk Pages'
    CODE = 'talk_pages_network'
    DIRECTED = False

    AVAILABLE_METRICS = {
        'Talk Page Edits': 'num_edits',
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
        }
    }

    USER_INFO = {
        'User ID': 'id',
        'User Name': 'label',
        'Absolute Birth': 'abs_birth',
        'Cluster': 'cluster',
        'Article Edits': 'article_edits'
    }


    def __init__(self, is_directed = False, graph = {}):
        super().__init__(is_directed = is_directed, graph = graph)

    
    def generate_from_pandas(self, df):
        user_per_page = {}
        mapper_v = {}
        mapper_e = {}
        count = 0

        dff = self.remove_non_talk_data(df)

        for _, r in dff.iterrows():
            # Nodes
            if not int(r['contributor_id']) in mapper_v:
                self.graph.add_vertex(count)
                mapper_v[int(r['contributor_id'])] = count
                self.graph.vs[count]['id'] = int(r['contributor_id'])
                self.graph.vs[count]['label'] = r['contributor_name']
                self.graph.vs[count]['num_edits'] = 0
                count += 1

            self.graph.vs[mapper_v[int(r['contributor_id'])]]['num_edits'] += 1

            # A page gets serveral contributors
            if not int(r['page_id']) in user_per_page:
                user_per_page[int(r['page_id'])] = {int(r['contributor_id'])}
            else:
                if int(r['contributor_id']) not in user_per_page[r['page_id']]:
                    user_per_page[r['page_id']].add(int(r['contributor_id']))

        count = 0
        # Edges
        for _, p in user_per_page.items():
            for u1 in p:
                for u2 in p:
                    if u1 == u2:
                        continue
                    k_edge = (u1 << 32) + u2
                    if k_edge in mapper_e:
                        self.graph.es[mapper_e[k_edge]]['weight'] += 1
                        continue

                    self.graph.add_edge(mapper_v[u1], mapper_v[u2])
                    mapper_e[k_edge] = count
                    count += 1
                    self.graph.es[mapper_e[k_edge]]['weight'] = 1
                    self.graph.es[mapper_e[k_edge]]['id'] = k_edge
                    self.graph.es[mapper_e[k_edge]]['source'] = u1
                    self.graph.es[mapper_e[k_edge]]['target'] = u2
    

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