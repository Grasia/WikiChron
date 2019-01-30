"""

 Author: Youssef El Faqir El Rhazoui
 Date: 13/12/2018
 Distributed under the terms of the GPLv3 license.

"""

from igraph import Graph, ClusterColoringPalette
from colormap.colors import rgb2hex

class BaseNetwork(Graph):

    NAME = 'Base Network'
    CODE = 'base_network'

    def __init__(self, is_directed = False, page_rank = [], num_communities = -1,
                graph = {}):
        if not graph:
            super().__init__(directed=is_directed)
        else:
            super().__init__(n = graph['n'], edges = graph['edges'], 
                directed = graph['directed'], graph_attrs = graph['graph_attrs'],
                vertex_attrs = graph['vertex_attrs'], edge_attrs = graph['edge_attrs'])
            
        self.page_rank = page_rank
        self.num_communities = num_communities


    def init_network(self):
        """
        Constructs an instance of this network type.
        Use this instead of the default constructor
        """
        return __init_(self)


    def __getnewargs_ex__(self):
        """
        A function to write and read objects with pickle.
        This function is called by __new__() upon unpickling.

        Return: A pair (args, kwargs) where args is a tuple of positional
                arguments and kwargs a dictionary of named arguments for 
                constructing the object
        """
        raise NotImplementedError('__getnewargs_ex__ is not implemented')


    def generate_from_pandas(self, data):
        """
        Generates a graph from a pandas data

        Parameters:
            -data: A pandas object with the wiki info (read from csv),
                   must be order by timestamp

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


    def filter_by_time(self, t_filter):
        """
        Filter a network by a date

        Parameters:
            -t_filter: a time in seconds to filter the network

        Return:
            A Network object with the filter applied
        """
        raise NotImplementedError('filter_by_timestamp is not implemented')

    def copy_and_write_gml(self, file):
        """
        This function clear the network atributes instead to write an gml file
        Parameters:
            file: path to save
        """
        raise NotImplementedError('write_gml is not implemented')

    def calculate_page_rank(self):
        """
        Calculates the network pageRank 
        """
        self.page_rank = self.pagerank(directed=self.is_directed())

    def calculate_communities(self):
        """
        Calculates communities and assigns a color per community
        """
        mod = self.community_multilevel(weights='weight')
        self.num_communities = len(mod)
        pal = ClusterColoringPalette(len(mod))
        self.vs['cluster_color'] = list(map(lambda x: rgb2hex(x[0],x[1],x[2], normalised=True), 
            pal.get_many(mod.membership)))