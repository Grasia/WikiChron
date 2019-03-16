"""
 Author: Youssef El Faqir El Rhazoui
 Date: 13/Dec/2018
 Distributed under the terms of the GPLv3 license.
"""

import abc
import pandas as pd
from igraph import Graph, ClusterColoringPalette
from colormap.colors import rgb2hex

class BaseNetwork(metaclass=abc.ABCMeta):

    NAME = 'Base Network'
    CODE = 'base_network'


    def __init__(self, is_directed = False, graph = {},):
        if not graph:
            self.graph = Graph(directed=is_directed)
        else:
            self.graph = graph


    @abc.abstractmethod
    def generate_from_pandas(self, df: pd.DataFrame):
        """
        Generates a graph from a pandas data

        Parameters:
            -df: A pandas object with the wiki info (read from csv),
                   must be order by timestamp
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
    def get_available_metrics(self) -> dict:
        """
        Return a dict with the metrics
        """
        pass


    @abc.abstractclassmethod
    def get_user_info(self) -> dict:
        """
        Return a dict with the user info
        """
        pass


    @abc.abstractmethod
    def add_graph_attrs(self):
        """
        Calculates and adds the graph attrs 
        """
        pass


    @abc.abstractclassmethod
    def get_secondary_metrics(cls) -> dict:
        """
        Returns a dict with the metrics, the dict must get the following structure:
            dict = {
                'Metric name well formatted': {
                    'key': 'a vertex key',
                    'max': 'a graph key',
                    'min': 'a graph key'
                }
            }
        """
        pass


    def to_cytoscape_dict(self) -> dict:
        """
        Transform a network to cytoscape dict

        Return:
            A dict with the cytoscape structure, graph attrs are keys, 
            and the cyto. elements are in the key 'network'
        """
        di_net = {}
        network = []

        # node attrs
        for node in self.graph.vs:
            data = {'data': {}}
            for attr in self.graph.vs.attributes():
                data['data'][attr] = node[attr]
            network.append(data)

        # edge attrs
        for edge in self.graph.es:
            data = {'data': {}}
            for attr in self.graph.es.attributes():
                data['data'][attr] = edge[attr]
            network.append(data)

        # graph attrs
        for attr in self.graph.attributes():
            di_net[attr] = self.graph[attr]

        di_net['network'] = network
        return di_net


    def calculate_metrics(self):
        """
        A method which calculate the available metrics 
        """
        self.calculate_page_rank()
        self.calculate_betweenness()
        self.calculate_assortativity_degree()
        self.calculate_communities()


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
            p_r = 0.0
            if not 'weight' in self.graph.es.attributes():
                p_r = self.graph.pagerank(directed=self.graph.is_directed())    
            else:
                p_r = self.graph.pagerank(directed=self.graph.is_directed(), 
                    weights = 'weight')

            self.graph.vs['page_rank'] = list(map(lambda x: "{0:.5f}".format(x), p_r))


    def calculate_betweenness(self):
        """
        Calculates the network betweenness
        """
        if not 'betweenness' in self.graph.vs.attributes():
            bet = 0.0
            if not 'weight' in self.graph.es.attributes():
                bet = self.graph.betweenness(directed=self.graph.is_directed())    
            else:
                bet = self.graph.betweenness(directed=self.graph.is_directed(), 
                    weights = 'weight')

            self.graph.vs['betweenness'] = list(map(lambda x: "{0:.5f}".format(x), bet))


    def calculate_communities(self):
        """
        Calculates communities and assigns a color per community
        """
        if not 'n_communities' in self.graph.attributes():
            if not 'weight' in self.graph.es.attributes():
                mod = self.graph.community_multilevel()
            else:
                mod = self.graph.community_multilevel(weights='weight')
                
            self.graph.vs['cluster'] = mod.membership
            self.graph['n_communities'] = len(mod)
            pal = ClusterColoringPalette(len(mod))
            self.graph.vs['cluster_color'] = list(map(lambda x: rgb2hex(x[0],x[1],x[2], normalised=True),
                pal.get_many(mod.membership)))


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
                assortativity = "{0:.5f}".format(assortativity)

            self.graph['assortativity_degree'] = assortativity


    def get_degree_distribution(self) -> (list, list):
        """
        It returns the degree distribution
        """
        ##########
        # TODO Check if it s directed
        ##########
        # Let's count the number of each degree
        p_k = [0 for i in range(0, self.graph.maxdegree()+1)]
        for x in self.graph.degree(): p_k[x] += 1
        # Now, we are gonna clean the 0's
        k = [i for i in range(0, self.graph.maxdegree()+1) if p_k[i] > 0]
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
        self.generate_from_pandas(dff)
        self.calculate_metrics()
        self.add_others(dff)
        self.add_graph_attrs()


    def filter_by_time(self, df: pd.DataFrame, lower_bound = '',
        upper_bound = '') -> pd.DataFrame:
        
        dff = df
        if lower_bound and upper_bound:
            dff = df[lower_bound <= df['timestamp']]
            dff = dff[dff['timestamp'] <= upper_bound]

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

    
    def calculate_edits(self, df: pd.DataFrame, type: str):
        """
        This function adds as a vertex attr the edits from other namespace
        type parameter only accept {talk, article, user_talk}
        """
        if 'id' not in self.graph.vs.attributes():
            return

        key = 'edits'
        if type == 'talk':
            dff = self.remove_non_talk_data(df)
            key = f'{type}_{key}'
        elif type == 'article':
            dff = self.remove_non_article_data(df)
            key = f'{type}_{key}'
        elif type == 'user_talk':
            dff = self.remove_non_user_talk_data(df)
            key = f'{type}_{key}'
        else:
            raise Exception(f'type: {type} is not defined')

        mapper = {self.graph.vs[i]['id']: i for i in range(len(self.graph.vs['id']))}
        edits = [0 for i in range(len(self.graph.vs['id']))]
        for _, row in dff.iterrows():
            if row['contributor_id'] in mapper.keys():
                edits[mapper[row['contributor_id']]] += 1

        self.graph.vs[key] = edits