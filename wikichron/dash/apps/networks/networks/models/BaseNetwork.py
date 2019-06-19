"""
 Author: Youssef El Faqir El Rhazoui
 Date: 13/Dec/2018
 Distributed under the terms of the GPLv3 license.
"""

import abc
from datetime import datetime
import pandas as pd
from igraph import Graph, ClusterColoringPalette, VertexClustering,\
    WEAK
from colormap.colors import rgb2hex
from math import log1p as log
import inequality_coefficients as ineq
import numpy as np

from .fix_dendrogram import fix_dendrogram


class BaseNetwork(metaclass=abc.ABCMeta):

    NAME = 'Base Network'
    CODE = 'base_network'
    DIRECTED = False

# CHANGE NAME
    NODE_METRICS_TO_PLOT = {
        'Tenure in the wiki': {
            'key': 'birth_value',
            'max': 'max_birth_value',
            'min': 'min_birth_value'
        },
        'Degree': {
            'key': 'degree',
            'max': 'max_degree',
            'min': 'min_degree'
        },
        'In-degree': {
            'key': 'indegree',
            'max': 'max_indegree',
            'min': 'min_indegree'
        },
        'Out-degree': {
            'key': 'outdegree',
            'max': 'max_outdegree',
            'min': 'min_outdegree'
        },
        'Closeness': {
            'key': 'closeness',
            'max': 'max_closeness',
            'min': 'min_closeness'
        },
        'Betweenness': {
            'key': 'betweenness',
            'max': 'max_betweenness',
            'min': 'min_betweenness'
        },
        'Page rank': {
            'key': 'page_rank',
            'max': 'max_page_rank',
            'min': 'min_page_rank'
        }
    }

    EDGE_METRICS_TO_PLOT = {
        'Weight': {
            'key': 'weight',
            'min': 'min_weight',
            'max': 'max_weight',
        }
    }

    NETWORK_STATS = {
        'Nodes': 'num_nodes',
        'Edges': 'num_edges',
        'Connected comp.': 'components',
        'Clusters': 'n_communities',
        'Density': 'density',
        'Assortativity': 'assortativity_degree',
        'Gini of betwee.': 'gini_betweenness',
        'Gini of close.': 'gini_closeness',
        'Gini of deg.': 'gini_degree',
        'Gini of in-deg.': 'gini_indegree',
        'Gini of out-deg.': 'gini_outdegree'
    }


    def __init__(self, is_directed = False, graph = {}, alias = ''):
        if not graph:
            self.graph = Graph(directed=is_directed)
        else:
            self.graph = graph

        self.alias = alias


    @abc.abstractmethod
    def generate_from_pandas(self, df: pd.DataFrame):
        """
        Fill the igraph attribute from pandas data

        Parameters:
            -df: A pandas object with the wiki info (coming from the csv file),
                   must be ordered by timestamp
        """
        pass


    @abc.abstractmethod
    def get_metric_dataframe(self, metric: str) -> pd.DataFrame:
        """
        This function generates a dateframe with 2 cols, the node name
        and a node metric value.
        Prarameters:
            - metric: an existing metric in the network
        Return:
            if metric exist a dataframe, if not None 
        """
        pass


    @abc.abstractclassmethod
    def get_metric_header(self, metric: str) -> list:
        """
        Returns a list with the header keys of the function get_metric_dataframe
        """
        pass


    @abc.abstractclassmethod
    def get_user_info(self) -> dict:
        """
        Return a dict with the user info
        """
        pass


    @abc.abstractclassmethod
    def get_node_name(self) -> dict:
        pass


    @abc.abstractclassmethod
    def is_directed(cls) -> bool:
        pass


    @abc.abstractclassmethod
    def get_network_stats(cls) -> dict:
        pass


    @abc.abstractclassmethod
    def get_metrics_to_plot(cls) -> dict:
        """
        This is used to clean NODE_METRICS_TO_PLOT
        """
        pass


    @abc.abstractclassmethod
    def get_metrics_to_show(cls) -> dict:
        """
        This is used to clean and prepare NODE_METRICS_TO_PLOT in order to show the data
        """
        pass


    @abc.abstractclassmethod
    def get_node_metrics(cls):
        pass


    @classmethod
    def remove_non_directed_node_metrics(cls, metrics):
        if 'Degree' in metrics:
            del metrics['Degree']


    @classmethod
    def remove_directed_node_metrics(cls, metrics):
        if 'In-degree' in metrics:
            del metrics['In-degree']
        if 'Out-degree' in metrics:
            del metrics['Out-degree']


    def add_graph_attrs(self):
        """
        Calculates and adds the graph attrs
        """
        self.graph['num_nodes'] = self.graph.vcount()
        self.graph['num_edges'] = self.graph.ecount()


    def to_cytoscape_dict(self) -> dict:
        """
        Transform a network to cytoscape dict

        Return:
            A dict with the cytoscape structure, graph attrs are keys, 
            and the cyto. elements are in the key 'network'
        """
        di_net = {}
        network = []
        metrics_to_plot = [val for key, val in self.NODE_METRICS_TO_PLOT.items()]
        metrics_to_plot = metrics_to_plot + [val for key, val in self.EDGE_METRICS_TO_PLOT.items()]
        log_keys = {metric['key'] for metric in metrics_to_plot if 'log' in metric.keys()}

        # node attrs
        for node in self.graph.vs:
            data = {'data': {}}
            for attr in self.graph.vs.attributes():
                val = node[attr]
                if attr in log_keys:
                    data['data'][f'{attr}_log'] = int(log(val)*100)

                data['data'][attr] = val

            network.append(data)

        # edge attrs
        for edge in self.graph.es:
            data = {'data': {}}
            for attr in self.graph.es.attributes():
                val = edge[attr]
                if attr == 'id':
                    continue
                if attr in log_keys:
                    data['data'][f'{attr}_log'] = int(log(val)*100)

                data['data'][attr] = val
            network.append(data)

        # graph attrs
        for attr in self.graph.attributes():
            di_net[attr] = self.graph[attr]

        # add max min metrics to plot
        _max = 0
        _min = 0
        for metric in metrics_to_plot:
            if metric['key'] in self.graph.vs.attributes() and len(self.graph.vs[metric['key']]):
                _max = max(self.graph.vs[metric['key']])
                _min = min(self.graph.vs[metric['key']])
            elif metric['key'] in self.graph.es.attributes() and len(self.graph.es[metric['key']]):
                _max = max(self.graph.es[metric['key']])
                _min = min(self.graph.es[metric['key']])

            if 'log' in metric.keys():
                _max = int(log(_max)*100)
                _min = int(log(_min)*100)

            di_net[metric['max']] = _max
            di_net[metric['min']] = _min


        di_net['network'] = network
        return di_net


    def write_gml(self, file: str):
        """
        Writes a gml file
        Parameters:
            file: path to save
        """
        self.graph.write(f=file, format='gml')


    def calculate_page_rank(self):
        """
        Calculates the network pageRank
        """
        if not 'page_rank' in self.graph.vs.attributes():
            weight = 'weight' if 'weight' in self.graph.es.attributes() else None
            p_r = self.graph.pagerank(directed=self.graph.is_directed(), 
                    weights = weight)

            self.graph.vs['page_rank'] = list(map(lambda x: float(f"{x:.4f}"), p_r))


    def calculate_betweenness(self):
        """
        Calculates the network betweenness
        """
        if not 'betweenness' in self.graph.vs.attributes():
            weight = 'weight' if 'weight' in self.graph.es.attributes() else None
            bet = self.graph.betweenness(directed=self.graph.is_directed(), 
                weights = weight)

            self.graph.vs['betweenness'] = list(map(lambda x: float(f"{x:.4f}"), bet))


    def calculate_gini_betweenness(self):
        if 'betweenness' in self.graph.vs.attributes() and 'gini_betweenness'\
            not in self.graph.attributes():
            gini = ineq.gini_corrected(self.graph.vs['betweenness'])
            value = 'nan'
            if gini is not np.nan:
                value = f"{gini:.2f}"

            self.graph['gini_betweenness'] = value


    def calculate_degree(self):
        if self.graph.is_directed() and 'indegree' not in self.graph.vs:
            self.graph.vs['indegree'] = self.graph.indegree()
            self.graph.vs['outdegree'] = self.graph.outdegree()
        elif 'degree' not in self.graph.vs:
            self.graph.vs['degree'] = self.graph.degree()


    def calculate_gini_degree(self):
        if self.graph.is_directed() and 'gini_indegree' not in\
            self.graph.attributes():

            gini = ineq.gini_corrected(self.graph.vs['indegree'])
            value = 'nan'
            if gini is not np.nan:
                value = value = f"{gini:.2f}"
            self.graph['gini_indegree'] = value
            gini = ineq.gini_corrected(self.graph.vs['outdegree'])
            value = 'nan'
            if gini is not np.nan:
                value = value = f"{gini:.2f}"
            self.graph['gini_outdegree'] = value

        elif 'gini_degree' not in self.graph.attributes():
            gini = ineq.gini_corrected(self.graph.vs['degree'])
            value = 'nan'
            if gini is not np.nan:
                value = value = f"{gini:.2f}"
            self.graph['gini_degree'] = value


    def calculate_communities(self):
        """
        Calculates communities and assigns a color per community
        """
        if not 'n_communities' in self.graph.attributes():
            weight = 'weight' if 'weight' in self.graph.es.attributes() else None
            # igraph bug: https://github.com/igraph/python-igraph/issues/17
            try:
                v_d = self.graph.community_walktrap(weights=weight, steps=6)
                mod = v_d.as_clustering()
            except:
                fix_dendrogram(self.graph, v_d)
                mod = v_d.as_clustering()

            self.graph.vs['cluster'] = mod.membership
            self.graph['n_communities'] = len(mod)
            pal = ClusterColoringPalette(len(mod))
            self.graph.vs['cluster_color'] = list(map(lambda x: rgb2hex(x[0],x[1],x[2],\
                normalised=True), pal.get_many(mod.membership)))


    def calculate_assortativity_degree(self):
        """
        Calculates the assortativity degree and put it as an graph attrb.
        * Reference:
            Newman MEJ: Assortative mixing in networks, Phys Rev Lett89:208701, 
            2002.@see:assortativity_degree()when thetypes are the vertex degrees
        """
        if not 'assortativity_degree' in self.graph.attributes():
            assortativity = self.graph.assortativity_degree(self.graph.is_directed())
            if assortativity:
                assortativity = f"{assortativity:.2f}"

            self.graph['assortativity_degree'] = assortativity


    def calculate_density(self):
        if not 'density' in self.graph.attributes():
            density = f'{self.graph.density():.2f}'
            self.graph['density'] = density


    def calculate_components(self):
        if not 'components' in self.graph.attributes():
            components = self.graph.clusters(mode=WEAK)
            self.graph['components'] = len(components.subgraphs())

    
    def calculate_closeness(self):
        if 'closeness' not in self.graph.vs.attributes() and 'weight'\
            in self.graph.es.attributes():

            rounder = lambda x: float(f"{x:.4f}")
            closeness = self.graph.closeness(weights='weight')
            closeness = list(map(rounder, closeness))
            self.graph.vs['closeness'] = closeness


    def calculate_gini_closeness(self):
        if 'closeness' in self.graph.vs.attributes() and 'gini_closeness'\
            not in self.graph.attributes():

            gini = ineq.gini_corrected(self.graph.vs['closeness'])
            if gini is not np.nan:
                self.graph['gini_closeness'] = f"{gini:.2f}"
        else:
            self.graph['gini_closeness'] = 'nan'

    
    def calculate_gini_article_edits(self):
        if 'article_edits' in self.graph.vs.attributes() and 'gini_article_edits'\
            not in self.graph.attributes():

            gini = ineq.gini_corrected(self.graph.vs['article_edits'])
            if gini is not np.nan:
                self.graph['gini_article_edits'] = f"{gini:.2f}"
        else:
            self.graph['gini_article_edits'] = 'nan'


    def calculate_gini_talk_edits(self):
        if 'talk_edits' in self.graph.vs.attributes() and 'gini_talk_edits'\
            not in self.graph.attributes():

            gini = ineq.gini_corrected(self.graph.vs['talk_edits'])
            if gini is not np.nan:
                self.graph['gini_talk_edits'] = f"{gini:.2f}"
        else:
            self.graph['gini_talk_edits'] = 'nan'


    def calculate_gini_user_talk_edits(self):
        if 'user_talks' in self.graph.vs.attributes() and 'gini_user_talks'\
            not in self.graph.attributes():

            gini = ineq.gini_corrected(self.graph.vs['user_talks'])
            if gini is not np.nan:
                self.graph['gini_user_talks'] = f"{gini:.2f}"
        else:
            self.graph['gini_user_talks'] = 'nan'


    def calculate_metrics(self):
        """
        A method which calculate the available metrics 
        """
        self.calculate_page_rank()
        self.calculate_betweenness()
        self.calculate_gini_betweenness()
        self.calculate_degree()
        self.calculate_gini_degree()
        self.calculate_assortativity_degree()
        self.calculate_communities()
        self.calculate_density()
        self.calculate_components()
        self.calculate_closeness()
        self.calculate_gini_closeness()
        self.calculate_gini_article_edits()
        self.calculate_gini_talk_edits()
        self.calculate_gini_user_talk_edits()


    def get_degree_distribution(self) -> (list, list):
        """
        Returns the degree distribution:
            if its directed is the sum of out and in degree
            if not its the out degree
        """

        degree = self.graph.degree()
        max_degree = self.graph.maxdegree()

        # Let's count the number of each degree
        p_k = [0 for i in range(0, max_degree + 1)]
        for x in degree: p_k[x] += 1
            
        # Now, we are gonna clean the 0's
        k = [i for i in range(0, max_degree + 1) if p_k[i] > 0]
        p_k = list(filter(lambda x: x > 0, p_k))

        return (k, p_k)


    def add_others(self, df):
        """
        It's used to add specific things (e.g. other metrics)
        """
        pass


    def build_network(self, df: pd.DataFrame, lower_bound: str, upper_bound: str):
        """
        This method is used to generate the network and its metrics and attrs
        """
        dff = self.filter_by_time(df, lower_bound, upper_bound)
        dff = self.filter_anonymous(dff)
        self.generate_from_pandas(dff)
        self.calculate_metrics()
        self.calculate_abs_longevity(df)
        self.add_others(dff)
        self.add_graph_attrs()


    def filter_by_time(self, df: pd.DataFrame, lower_bound = '',
        upper_bound = '') -> pd.DataFrame:

        dff = df
        if lower_bound and upper_bound:
            dff = dff[lower_bound <= dff['timestamp']]
            dff = dff[dff['timestamp'] <= upper_bound]

        return dff


    def filter_anonymous(self, df: pd.DataFrame) -> pd.DataFrame:
        dff = df
        if not dff.empty:
            dff = dff['Anonymous' != dff['contributor_name']]

        return dff


    def remove_non_article_data(self, df: pd.DataFrame) -> pd.DataFrame:
       """
          Filter out all edits made on non-article pages.

          df -- data to be filtered.
          Return a dataframe derived from the original but with all the
             editions made in non-article pages removed
       """
       # namespace 0 => wiki article
       return df[df['page_ns'] == 0]


    def remove_non_talk_data(self, df: pd.DataFrame) -> pd.DataFrame:
       """
          Filter out all edits made on non-talk pages.

          df -- data to be filtered.
          Return a dataframe derived from the original but with all the
             editions made in non-talk pages removed
       """
       # namespace 1 => wiki talk pages
       return df[df['page_ns'] == 1]


    def remove_non_user_talk_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
          Filter out all edits made on non-user-talk pages.

          df -- data to be filtered.
          Return a dataframe derived from the original but with all the
             editions made in non-user-talk pages removed
        """
        # namespace 3 => wiki user talk pages
        return df[df['page_ns'] == 3]

    
    def calculate_edits(self, df: pd.DataFrame, type_e: str):
        """
        This function adds as a vertex attr the edits from other namespace
        type_e parameter only accept {talk, article, user_talk}
        """
        allowed_types = {'talk', 'article', 'user_talk'}
        if type_e not in allowed_types:
            raise Exception(f"Not allowed type: {type_e}, it must be {allowed_types}")

        if 'label' not in self.graph.vs.attributes():
            return

        key = 'edits'
        if type_e == 'talk':
            dff = self.remove_non_talk_data(df)
            key = f'{type_e}_{key}'
        elif type_e == 'article':
            dff = self.remove_non_article_data(df)
            key = f'{type_e}_{key}'
        elif type_e == 'user_talk':
            raise Exception(f'type: {type_e} is not implemented yet')
        else:
            raise Exception(f'type: {type_e} is not defined')

        mapper = {self.graph.vs[i]['label']: i for i in range(self.graph.vcount())}
        edits = [0 for i in range(self.graph.vcount())]
        pages = [set() for _ in range(self.graph.vcount())]
        for _, row in dff.iterrows():
            if row['contributor_name'] in mapper.keys():
                edits[mapper[row['contributor_name']]] += 1
                pages[mapper[row['contributor_name']]].add(int(row['page_id']))

        sizer = lambda x: len(x)
        pages = list(map(sizer, pages))
        self.graph.vs[f"{type_e}s"] = pages
        self.graph.vs[key] = edits


    def calculate_abs_longevity(self, df: pd.DataFrame):
        """
        Calculates the birth of all the vertex without filter_by_time 
        """
        inverter = lambda x: 1/x*1000
        max_date = 0
        for node in self.graph.vs:
            dff = df[node['label'] == df['contributor_name']]
            if not dff.empty:
                row = dff.iloc[0]
                node['birth'] = datetime.strftime(row['timestamp'], "%d/%b/%Y")
                node['birth_value'] = int(datetime.strptime(
                    str(row['timestamp']), "%Y-%m-%d %H:%M:%S").strftime('%s'))

                # this is a weak solution to avoid users with no activity
                if max_date < node['birth_value']:
                    max_date = node['birth_value']
            else:
                node['birth'] = 'Not available'
                node['birth_value'] = max_date
        
        if 'birth_value' in self.graph.vs.attributes():
            self.graph.vs['birth_value'] = list(map(inverter, self.graph.vs['birth_value']))