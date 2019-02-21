"""

 Author: Youssef El Faqir El Rhazoui
 Date: 13/Dec/2018
 Distributed under the terms of the GPLv3 license.

"""

from igraph import Graph, ClusterColoringPalette
from colormap.colors import rgb2hex

class BaseNetwork():

    NAME = 'Base Network'
    CODE = 'base_network'

    def __init__(self, is_directed = False, page_rank = [], 
            num_communities = -1, first_entry = None, 
            last_entry = None, graph = {},):

        if not graph:
            self.graph = Graph(directed=is_directed)
        else:
            self.graph = graph

        self.page_rank = page_rank
        self.num_communities = num_communities
        self.first_entry = first_entry
        self.last_entry = last_entry 


    def init_network(self):
        """
        Constructs an instance of this network type.
        Use this instead of the default constructor
        """
        return __init_(self)


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
        Return: A graph with the network representation.
        """
        raise NotImplementedError('generate_from_pandas is not implemented')


    def to_cytoscape_dict(self):
        """
        Transform this network to cytoscape dict

        Return:
            A dict with the cytoscape structure
        """
        raise NotImplementedError('to_cytoscape_dict is not implemented')


    def copy_and_write_gml(self, file):
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
        if not self.page_rank:
            self.page_rank = self.graph.pagerank(directed=self.graph.is_directed())


    def calculate_communities(self):
        """
        Calculates communities and assigns a color per community
        """
        if self.num_communities is -1:
            mod = self.graph.community_multilevel(weights='weight')
            self.num_communities = len(mod)
            pal = ClusterColoringPalette(len(mod))
            self.graph.vs['cluster_color'] = list(map(lambda x: rgb2hex(x[0],x[1],x[2], normalised=True),
                pal.get_many(mod.membership)))