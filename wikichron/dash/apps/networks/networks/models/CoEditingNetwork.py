"""

 Author: Youssef El Faqir El Rhazoui
 Date: 13/Dec/2018
 Distributed under the terms of the GPLv3 license.

"""

import pandas as pd
from .BaseNetwork import BaseNetwork


class CoEditingNetwork(BaseNetwork):
    """
    This network is based on the editors cooperation, this means, the nodes
    are user from a wiki, and a edge will link two nodes if they edit the same
    page. As well, this network has the following args:

        - Node:
            * id: user id on the wiki
            * label: the user name with id contributor_id on the wiki
            * num_edits: the number of edit in the whole wiki
            * abs_birth: the first edit in the whole network

        - Edge:
            * source: contributor_id
            * target: contributor_id
            * weight: the number of cooperation in different pages on the wiki,
                      differents editions on the same page computes only once.

    """
    NAME = 'Co-Editing'
    CODE = 'co_editing_network'
    DIRECTED = False

    # only metrics for the ranking
    AVAILABLE_METRICS = {
        'Article Edits': 'num_edits',
        'Betweenness': 'betweenness',
        'Page Rank': 'page_rank'
    }

    NODE_METRICS_TO_PLOT = {
        'Article Edits': {
            'key': 'num_edits',
            'max': 'max_node_size',
            'min': 'min_node_size'
        },
        'Lifespan': {
            'key': 'abs_birth_int',
            'max': 'max_abs_birth_int',
            'min': 'min_abs_birth_int'
        },
        'Talk Edits': {
            'key': 'talk_edits',
            'max': 'max_talk_edits',
            'min': 'min_talk_edits'
        }
    }

    USER_INFO = {
        #'User ID': 'id',
        'Birth': 'abs_birth',
        'Cluster #': 'cluster',
        'Talk Page Edits': 'talk_edits',
    }

    NODE_NAME = {
        'User': 'label'
    }


    def __init__(self, is_directed = False, graph = {}, alias = ''):
        super().__init__(is_directed, graph, alias)


    def generate_from_pandas(self, df):
        user_per_page = {}
        mapper_v = {}
        mapper_e = {}
        count = 0
        dff = self.remove_non_article_data(df)

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
                if int(r['contributor_id']) not in user_per_page[int(r['page_id'])]:
                    user_per_page[int(r['page_id'])].add(int(r['contributor_id']))

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
    def get_metric_header(cls, metric: str) -> list:
        header = list()
        if metric in cls.AVAILABLE_METRICS:
            header = [{'name': 'User', 'id': 'User'}, 
                {'name': metric, 'id': metric}]

        return header


    @classmethod
    def get_available_metrics(cls) -> dict:
        return cls.AVAILABLE_METRICS


    @classmethod
    def get_user_info(cls) -> dict:
        return cls.USER_INFO


    @classmethod
    def get_node_name(cls) -> dict:
        return cls.NODE_NAME


    @classmethod
    def get_metrics_to_plot(cls) -> dict:
        return cls.NODE_METRICS_TO_PLOT


    @classmethod
    def is_directed(cls):
        return cls.DIRECTED


    @classmethod
    def get_network_description(cls) -> dict:
        desc = {}
        desc['min_node_color'] = 'Lowest value in selected metric'
        desc['max_node_color'] = 'Highest value in selected metric'
        desc['min_node_size'] = 'A low edition in articles'
        desc['max_node_size'] = 'A high edition in articles'
        desc['min_edge_size'] = 'A weak interaction in the wiki'
        desc['max_edge_size'] = 'A strong interaction in the wiki'
        return desc


    def add_others(self, df):
        self.calculate_edits(df, 'talk')
