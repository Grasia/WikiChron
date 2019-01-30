"""
   CoEditingCytoscapeDecorator.py

   Descp: A class to implement the decorator pattern in order to make an 
     easier implementation of networks stylesheet

   Created on: 30/01/2019

   Copyright 2019 Youssef 'FRYoussef' El Faqir el Rhazoui <f.r.youssef@hotmail.com>
"""
from .BaseCytoscapeDecorator import BaseCytoscapeDecorator

class CoEditingCytoscapeDecorator(BaseCytoscapeDecorator):


	def __init__(self, stylesheet):
		super().__init__(stylesheet)


	def color_nodes(self, network):
		if network['oldest_user'] == network['newest_user']:
			self.stylesheet.color_nodes(network)
			return

		self.stylesheet.cy_stylesheet[0]['style']['background-color'] = \
			f"mapData(first_edit, {network['oldest_user']}, \
			{network['newest_user']}, #64B5F6, #0D47A1)"


	def size_nodes(self, network):
		if network['user_min_edits'] == network['user_max_edits']:
			self.stylesheet.size_nodes(network)
			return

		self.stylesheet.cy_stylesheet[0]['style']['height'] = \
			f"mapData(num_edits, {network['user_min_edits']}, \
			{network['user_max_edits']}, 10, 60)"

		self.stylesheet.cy_stylesheet[0]['style']['width'] = \
			f"mapData(num_edits, {network['user_min_edits']}, \
			{network['user_max_edits']}, 10, 60)"

		self.size_font_labels(network)


	def size_font_labels(self, network):
		if network['user_min_edits'] == network['user_max_edits']:
			self.stylesheet.size_font_labels(network)
			return

		self.stylesheet.cy_stylesheet[0]['style']['font-size'] = \
			f"mapData(num_edits, {network['user_min_edits']}, \
			{network['user_max_edits']}, 7, 18)"


	def color_edges(self, _):
		self.stylesheet.cy_stylesheet[1]['style']['line-color'] = \
			'mapData(w_time, 0, 2, #9E9E9E, #000000)'


	def set_edges_opacity(self, _):
		self.stylesheet.cy_stylesheet[1]['style']['opacity'] = \
			'mapData(w_time, 0, 2, 0.4, 1)'


	def size_edges(self, network):
		if network['edge_min_weight'] == network['edge_max_weight']:
			self.stylesheet.size_edges(network)
			return

		self.stylesheet.cy_stylesheet[1]['style']['width'] = \
			f"mapData(weight, {network['edge_min_weight']}, \
			{network['edge_max_weight']}, 1, 10)"


	def all_transformations(self, network):
		self.color_nodes(network)
		self.size_nodes(network)
		self.color_edges(network)
		self.set_edges_opacity(network)
		self.size_edges(network)