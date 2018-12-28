"""

 Author: Youssef El Faqir El Rhazoui
 Date: 13/12/2018
 Distributed under the terms of the GPLv3 license.

"""

from igraph import Graph

class BaseNetwork(Graph):

    def __init__(self, is_directed = False):
        super().__init__(directed=is_directed)
        self.directed = is_directed
        self.code = 'base_network'
        self.name = 'Base Network'
        self.page_rank = []


    def init_network(self):
        """
        Constructs an instance of this network type.
        Use this instead of the default constructor
        """
        return __init_(self)


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


    def calculate_page_rank(self):
        """
        Calculates the network pageRank 
        """
        self.page_rank = self.pagerank(directed=self.directed)