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
            * talk_edits: The editions number in all talk pages
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

    NETWORK_STATS = BaseNetwork.NETWORK_STATS.copy()
    NETWORK_STATS['Gini of talk ed.'] = 'gini_talk_edits'
    NETWORK_STATS['Edited talk pages'] = 'wiki_talks'
    NETWORK_STATS['Talk page edits'] = 'wiki_talk_edits'

    NODE_METRICS_TO_PLOT = {
        'Talk page edits': {
            'key': 'talk_edits',
            'log': 'talk_edits_log',
            'max': 'max_talk_edits',
            'min': 'min_talk_edits'
        },
        'Edited talk pages': {
            'key': 'talks',
            'max': 'max_talks',
            'min': 'min_talks'
        },
        'Article edits': {
            'key': 'article_edits',
            'log': 'article_edits_log',
            'max': 'max_article_edits',
            'min': 'min_article_edits'
        },
        'Edited articles': {
            'key': 'articles',
            'log': 'articles_log',
            'max': 'max_articles',
            'min': 'min_articles'
        },
    }

    NODE_METRICS_TO_PLOT.update(BaseNetwork.NODE_METRICS_TO_PLOT.copy())

    USER_INFO = {
        #'User ID': 'id',
        'Registered since': 'birth',
        'Cluster #': 'cluster'
    }

    NODE_NAME = {
        'Editor': 'label'
    }


    def __init__(self, is_directed = False, graph = {}, alias = ''):
        super().__init__(is_directed, graph, alias)

    
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
                self.graph.vs[count]['talk_edits'] = 0
                self.graph.vs[count]['talks'] = {int(r['page_id'])}
                count += 1

            self.graph.vs[mapper_v[int(r['contributor_id'])]]['talk_edits'] += 1
            self.graph.vs[mapper_v[int(r['contributor_id'])]]['talks'].add(int(r['page_id']))

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
                    k_edge_2 = (u2 << 32) + u1
                    if k_edge in mapper_e:
                        self.graph.es[mapper_e[k_edge]]['weight'] += 1
                        continue
                    elif k_edge_2 in mapper_e:
                        #self.graph.es[mapper_e[k_edge_2]]['weight'] += 1
                        continue

                    self.graph.add_edge(mapper_v[u1], mapper_v[u2])
                    mapper_e[k_edge] = count
                    count += 1
                    self.graph.es[mapper_e[k_edge]]['weight'] = 1
                    self.graph.es[mapper_e[k_edge]]['id'] = k_edge
                    self.graph.es[mapper_e[k_edge]]['source'] = u1
                    self.graph.es[mapper_e[k_edge]]['target'] = u2

        # total pages per user 
        if 'talks' in self.graph.vs.attributes():
            talks = [len(node['talks']) for node in self.graph.vs]
            self.graph.vs['talks'] = talks

        # total pages
        self.graph['wiki_talks'] = len(user_per_page)
        self.graph['wiki_talk_edits'] = len(dff.index)
    

    def get_metric_dataframe(self, metric):
        metrics = TalkPagesNetwork.get_metrics_to_plot()

        if metrics[metric] in self.graph.vs.attributes()\
            and 'label' in self.graph.vs.attributes():

            df = pd.DataFrame({
                    'User': self.graph.vs['label'],
                    metric: self.graph.vs[metrics[metric]]
                    })
            return df

        return pd.DataFrame()


    def add_others(self, df):
        self.calculate_edits(df, 'article')


    @classmethod
    def get_metrics_to_plot(cls) -> dict:
        cls.remove_directed_node_metrics(cls.NODE_METRICS_TO_PLOT)
        metrics = dict()

        for k in cls.NODE_METRICS_TO_PLOT.keys():
            metrics[k] = cls.NODE_METRICS_TO_PLOT[k]['key']
        return metrics


    @classmethod
    def get_metrics_to_show(cls) -> dict:
        metrics = cls.get_metrics_to_plot().copy()
        del metrics['Tenure in the wiki']
        return metrics
        

    @classmethod
    def get_metric_header(cls, metric: str) -> list:
        metrics = cls.get_metrics_to_plot()
        header = list()
        if metric in metrics:
            header = [{'name': 'Editor', 'id': 'User'}, 
                {'name': metric, 'id': metric}]

        return header


    @classmethod
    def get_user_info(cls) -> dict:
        return cls.USER_INFO

    
    @classmethod
    def get_network_stats(cls) -> dict:
        return cls.NETWORK_STATS


    @classmethod
    def get_node_name(cls) -> dict:
        return cls.NODE_NAME


    @classmethod
    def is_directed(cls):
        return cls.DIRECTED


    @classmethod
    def get_node_metrics(cls):
        return cls.NODE_METRICS_TO_PLOT