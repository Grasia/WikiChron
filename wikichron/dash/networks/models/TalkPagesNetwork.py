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

    AVAILABLE_METRICS = {
        'Talk Pages Edit': 'num_edits',
        'Betweenness': 'betweenness',
        'Page Rank': 'page_rank'
    }

    SECONDARY_METRICS = {
        'Article Edits': {
            'key': 'article_edits',
            'max': 'max_article_edits',
            'min': 'min_article_edits'
        }
    }

    USER_INFO = {
        'User ID': 'id',
        'User Name': 'label',
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
            if r['contributor_name'] == 'Anonymous':
                continue

            # Nodes
            if not r['contributor_id'] in mapper_v:
                self.graph.add_vertex(count)
                mapper_v[r['contributor_id']] = count
                self.graph.vs[count]['id'] = r['contributor_id']
                self.graph.vs[count]['label'] = r['contributor_name']
                self.graph.vs[count]['num_edits'] = 0
                count += 1

            self.graph.vs[mapper_v[r['contributor_id']]]['num_edits'] += 1

            # A page gets serveral contributors
            if not r['page_id'] in user_per_page:
                user_per_page[r['page_id']] = \
                                {r['contributor_id']: [r['timestamp']]}
            else:
                if r['contributor_id'] in user_per_page[r['page_id']]:
                    user_per_page[r['page_id']][r['contributor_id']]\
                                .append(r['timestamp'])
                else:
                    user_per_page[r['page_id']][r['contributor_id']] = \
                            [r['timestamp']]

        count = 0
        # Edges
        for _, p in user_per_page.items():
            aux = {}
            for k_i, v_i in p.items():
                for k_j in aux.keys():
                    if f'{k_i}{k_j}' in mapper_e:
                        self.graph.es[mapper_e[f'{k_i}{k_j}']]['weight'] += 1
                        continue
                    if f'{k_j}{k_i}' in mapper_e:
                        self.graph.es[mapper_e[f'{k_j}{k_i}']]['weight'] += 1
                        continue

                    self.graph.add_edge(mapper_v[k_i], mapper_v[k_j])
                    mapper_e[f'{k_i}{k_j}'] = count
                    count += 1
                    self.graph.es[mapper_e[f'{k_i}{k_j}']]['weight'] = 1
                    self.graph.es[mapper_e[f'{k_i}{k_j}']]['id'] = f'{k_i}{k_j}'
                    self.graph.es[mapper_e[f'{k_i}{k_j}']]['source'] = k_i
                    self.graph.es[mapper_e[f'{k_i}{k_j}']]['target'] = k_j

                aux[k_i] = v_i

        return
    

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
        self.graph['num_nodes'] = self.graph.vcount()
        self.graph['num_edges'] = self.graph.ecount()
        if 'num_edits' in self.graph.vs.attributes():
            self.graph['max_node_size'] = max(self.graph.vs['num_edits'])
            self.graph['min_node_size'] = min(self.graph.vs['num_edits'])
        if 'article_edits' in self.graph.vs.attributes():
            self.graph['max_article_edits'] = max(self.graph.vs['article_edits'])
            self.graph['min_article_edits'] = min(self.graph.vs['article_edits'])
        if 'weight' in self.graph.es.attributes():
            self.graph['max_edge_size'] = max(self.graph.es['weight'])
            self.graph['min_edge_size'] = min(self.graph.es['weight'])

    
    def add_others(self, df):
        self.calculate_edits(df, 'article')