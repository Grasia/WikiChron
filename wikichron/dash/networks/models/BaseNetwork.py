"""

 Author: Youssef El Faqir El Rhazoui
 Date: 13/Dec/2018
 Distributed under the terms of the GPLv3 license.

"""
import abc
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
    def generate_from_pandas(self, df, lower_bound, upper_bound):
        """
        Generates a graph from a pandas data

        Parameters:
            -df: A pandas object with the wiki info (read from csv),
                   must be order by timestamp

            -lower_bound: a formated string "%Y-%m-%d %H:%M:%S", 
                    to filter by time the df 
            -upper_bound: a formated string "%Y-%m-%d %H:%M:%S", 
                    to filter by time the df
        """
        pass


    @abc.abstractmethod
    def get_metric_dataframe(self, metric: str):
        """
        This function generates a dateframe with 2 cols, the node name
        and a node metric value.
        Prarameters:
            - metric: an existing metric in the network
        Return:
            if metric exist a dataframe, if not None 
        """
        pass

    
    @abc.abstractmethod
    def get_available_metrics(self) -> dict:
        """
        Return a dict with the metrics
        """
        pass


    @abc.abstractmethod
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


    def to_cytoscape_dict(self):
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


    def write_gml(self, file):
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


    def get_degree_distribution(self):
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

    
    def build_network(self, df, lower_bound: str, upper_bound: str):
        """
        This method is used to generate the network and its metrics and attrs
        """
        self.generate_from_pandas(df, lower_bound, upper_bound)
        self.add_graph_attrs()
        self.calculate_metrics()