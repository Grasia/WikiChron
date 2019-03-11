"""

 Author: Youssef El Faqir El Rhazoui
 Date: 13/Dec/2018
 Distributed under the terms of the GPLv3 license.

"""

import pandas as pd
import numpy
import math
from datetime import datetime

from .BaseNetwork import BaseNetwork

class CoEditingNetwork(BaseNetwork):
    """
    This network is based on the editors cooperation, this means, the nodes
    are user from a wiki, and a edge will link two nodes if they edit the same
    page. As well, this network has the following args:

        - Node:
            * contributor_id: id user on the wiki
            * label: the user name with id contributor_id on the wiki
            * num_edits: the number of edit in the whole wiki
            * first_edit: this is a datetime object with the first edition
            * last_edit: this is a datetime object with the last edition

        - Edge:
            * source: contributor_id
            * target: contributor_id
            * weight: the number of cooperation in different pages on the wiki,
                      differents editions on the same page computes only once.

    """

    #aprox 1 month = 30 days
    TIME_DIV = 60 * 60 * 24 * 30
    TIME_BOUND = 24 * 15
    NAME = 'Co-Editing'
    CODE = 'co_editing_network'
    AVAILABLE_METRICS = {
            'Page Rank': 'page_rank',
            'Number of Edits': 'num_edits',
            'Betweenness': 'betweenness'
        }

    USER_INFO = {
        'Wiki ID': 'contributor_id',
        'User Name': 'label',
        'Edits Number': 'num_edits',
        'First Edit': 'first_edit',
        'Last Edit': 'last_edit'
    }


    def __init__(self, is_directed = False, graph = {},
        first_entry = None, last_entry = None):

        super().__init__(is_directed = is_directed, first_entry = first_entry,
            last_entry = last_entry, graph = graph)


    def generate_from_pandas(self, df, lower_bound = '', upper_bound = ''):
        user_per_page = {}
        mapper_v = {}
        mapper_e = {}
        count = 0

        if lower_bound:
            df = df[lower_bound <= df['timestamp']]
            df = df[df['timestamp'] <= upper_bound]
        df = self.remove_non_article_data(df)

        for index, r in df.iterrows():
            if r['contributor_name'] == 'Anonymous':
                continue

            if not self.first_entry:
                self.first_entry = r['timestamp']

            self.last_entry = r['timestamp']

            # Nodes
            if not r['contributor_id'] in mapper_v:
                self.graph.add_vertex(count)
                mapper_v[r['contributor_id']] = count
                self.graph.vs[count]['contributor_id'] = r['contributor_id']
                self.graph.vs[count]['label'] = r['contributor_name']
                self.graph.vs[count]['num_edits'] = 0
                self.graph.vs[count]['first_edit'] = r['timestamp']
                count += 1

            self.graph.vs[mapper_v[r['contributor_id']]]['num_edits'] += 1
            self.graph.vs[mapper_v[r['contributor_id']]]['last_edit'] = r['timestamp']

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
        for k, p in user_per_page.items():
            aux = {}
            for k_i, v_i in p.items():
                for k_j, v_j in aux.items():
                    if f'{k_i}{k_j}' in mapper_e:
                        self.graph.es[mapper_e[f'{k_i}{k_j}']]['weight'] += 1
                        self.graph.es[mapper_e[f'{k_i}{k_j}']]['w_time'] += \
                            self.calculate_w_time(v_i[-1], v_j[-1])
                        continue
                    if f'{k_j}{k_i}' in mapper_e:
                        self.graph.es[mapper_e[f'{k_j}{k_i}']]['weight'] += 1
                        self.graph.es[mapper_e[f'{k_j}{k_i}']]['w_time'] += \
                            self.calculate_w_time(v_j[-1], v_i[-1])
                        continue

                    self.graph.add_edge(mapper_v[k_i], mapper_v[k_j])
                    mapper_e[f'{k_i}{k_j}'] = count
                    count += 1
                    self.graph.es[mapper_e[f'{k_i}{k_j}']]['weight'] = 1
                    self.graph.es[mapper_e[f'{k_i}{k_j}']]['w_time'] = \
                            self.calculate_w_time(v_i[-1], v_j[-1])
                    self.graph.es[mapper_e[f'{k_i}{k_j}']]['id'] = f'{k_i}{k_j}'
                    self.graph.es[mapper_e[f'{k_i}{k_j}']]['source'] = k_i
                    self.graph.es[mapper_e[f'{k_i}{k_j}']]['target'] = k_j

                aux[k_i] = v_i

        for e in self.graph.es:
            e['w_time'] = e['w_time'] / e['weight']
        return


    def to_cytoscape_dict(self):
        di_net = {}
        network = []
        min_v = float('Inf')
        max_v = -1

        for node in self.graph.vs:
            if min_v > node['num_edits']:
                min_v = node['num_edits']
            if max_v < node['num_edits']:
                max_v = node['num_edits']
            f_e = int(datetime.strptime(
                    str(node['first_edit']), "%Y-%m-%d %H:%M:%S").strftime('%s'))

            network.append({
                'data': {
                    'id': node['contributor_id'],
                    'label': node['label'],
                    'num_edits': node['num_edits'],
                    'first_edit': f_e,
                    'last_edit': node['last_edit'],
                    'page_rank': "{0:.5f}".format(node['page_rank'])
                        if 'page_rank' in self.graph.vs.attributes() else '',
                    'betweenness': "{0:.5f}".format(node['betweenness'])
                        if 'betweenness' in self.graph.vs.attributes() else '',
                    'cluster': node['cluster']
                        if 'cluster' in self.graph.vs.attributes() else '',
                    'cluster_color': node['cluster_color']
                        if 'cluster_color' in self.graph.vs.attributes() else ''
                }
            })

        di_net['user_max_edits'] = max_v
        di_net['user_min_edits'] = min_v
        min_v = float('Inf')
        max_v = -1
        for edge in self.graph.es:

            if min_v > edge['weight']:
                min_v = edge['weight']
            if max_v < edge['weight']:
                max_v = edge['weight']

            network.append({
                'data': {
                    'id': edge['id'],
                    'source': edge['source'],
                    'target': edge['target'],
                    'weight': edge['weight'],
                    'w_time': edge['w_time']
                }
            })
        f_e = 'Not entries'
        l_e = 'Not entries'

        if self.first_entry:
            f_e = int(datetime.strptime(str(self.first_entry),
                "%Y-%m-%d %H:%M:%S").strftime('%s'))
        if self.last_entry:
            l_e = int(datetime.strptime(str(self.last_entry),
                "%Y-%m-%d %H:%M:%S").strftime('%s'))

        di_net['first_entry'] = f_e
        di_net['last_entry'] = l_e
        di_net['edge_max_weight'] = max_v
        di_net['edge_min_weight'] = min_v
        di_net['num_nodes'] = self.graph.vcount()
        di_net['num_edges'] = self.graph.ecount()
        di_net['max_degree'] = self.graph.maxdegree()
        di_net['n_communities'] = self.graph['n_communities'] \
            if 'n_communities' in self.graph.attributes() else '...'
        di_net['assortativity'] = self.graph['assortativity_degree'] \
            if 'assortativity_degree' in self.graph.attributes() else '...'
        di_net['network'] = network
        return di_net


    def calculate_metrics(self):
        self.calculate_page_rank()
        self.calculate_betweenness()
        self.calculate_assortativity_degree()
        self.calculate_communities()


    def calculate_w_time(self, tsp1, tsp2):
        """
        Calculates the weight based on time between 2 editions

        Parameters:
            -tsp1: a timestamp
            -tsp2: a timestamp

        Returns: a number which represent the w_time
        """
        t1 = int(datetime.strptime(str(tsp1),
            "%Y-%m-%d %H:%M:%S").strftime('%s'))
        t2 = int(datetime.strptime(str(tsp2),
            "%Y-%m-%d %H:%M:%S").strftime('%s'))
        t_gap = math.fabs(t1 - t2)

        if t_gap == 0:
            return 2

        if t_gap > self.TIME_DIV:
            return self.TIME_DIV / t_gap

        return 1 + numpy.interp(
            self.TIME_DIV / t_gap, [1, self.TIME_BOUND], [0, 1])


    def remove_non_article_data(self, df):
       """
          Filter out all edits made on non-article pages.

          df -- data to be filtered.
          Return a dataframe derived from the original but with all the
             editions made in non-article pages removed
       """
       # namespace 0 => wiki article
       return df[df['page_ns'] == 0]


    def get_metric_dataframe(self, metric: str) -> pd.DataFrame:
        if self.AVAILABLE_METRICS[metric] in self.graph.vs.attributes():
            df = pd.DataFrame({
                    'User': self.graph.vs['label'],
                    metric: self.graph.vs[self.AVAILABLE_METRICS[metric]]
                    })
            return df

        return None


    @classmethod
    def get_available_metrics(cls) -> dict:
        return cls.AVAILABLE_METRICS


    @classmethod
    def get_user_info(cls) -> dict:
        return cls.USER_INFO
