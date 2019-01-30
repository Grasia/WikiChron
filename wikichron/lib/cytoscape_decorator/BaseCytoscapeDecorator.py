"""
   BaseCytoscapeDecorator.py

   Descp: A base class to implement the decorator pattern in order to make an 
     easier implementation of networks stylesheet

   Created on: 30/01/2019

   Copyright 2019 Youssef 'FRYoussef' El Faqir el Rhazoui <f.r.youssef@hotmail.com>
"""
import abc
from .Stylesheet import Stylesheet

class BaseCytoscapeDecorator(Stylesheet, metaclass=abc.ABCMeta):

	def __init__(self, stylesheet):
		self.stylesheet = stylesheet

	def color_nodes(self, network):
		self.stylesheet.color_nodes(network)

	def color_nodes_by_cluster(self):
		self.stylesheet.color_nodes_by_cluster()

	def size_nodes(self, network):
		self.stylesheet.size_nodes(network)
		self.size_font_labels(network)

	def size_font_labels(self, network):
		self.stylesheet.size_font_labels(network)

	def color_edges(self, network):
		self.stylesheet.color_edges(network)

	def set_edges_opacity(self, network):
		self.stylesheet.set_edges_opacity(network)

	def size_edges(self, network):
		self.stylesheet.size_edges(network)

	def set_label(self, text):
		self.stylesheet.set_label(text)

	@abc.abstractmethod
	def all_transformations(self, _):
		pass