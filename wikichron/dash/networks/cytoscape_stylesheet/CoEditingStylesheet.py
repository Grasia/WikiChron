"""
   CoEditingStylesheet.py

   Descp: A class to warp the cytoscape stylesheet for a co-editing network

   Created on: 30/01/2019

   Copyright 2019 Youssef 'FRYoussef' El Faqir el Rhazoui <f.r.youssef@hotmail.com>
"""
import abc

from .BaseStylesheet import BaseStylesheet


class CoEditingStylesheet(BaseStylesheet, metaclass=abc.ABCMeta):

	HIGHLIGHT_NODE = {
			"background-color": "#B10DC9",
            "border-color": "purple",
            "border-width": 2,
            "border-opacity": 1,
			"opacity": 1,
			"label": "data(label)",
            "color": "#B10DC9",
            "text-opacity": 1,
			"z-index": 9999
		}


	def __init__(self, cy_stylesheet = []):
		super().__init__(cy_stylesheet)


	def color_nodes(self, network):
		if network['first_entry'] == network['last_entry']:
			super().color_nodes(network)
			return

		self.cy_stylesheet[0]['style']['background-color'] = \
			f"mapData(first_edit, {network['first_entry']}, \
			{network['last_entry']}, #64B5F6, #0D47A1)"


	def size_nodes(self, network):
		if network['user_min_edits'] == network['user_max_edits']:
			super().size_nodes(network)
			return

		self.cy_stylesheet[0]['style']['height'] = \
			f"mapData(num_edits, {network['user_min_edits']}, \
			{network['user_max_edits']}, 10, 60)"

		self.cy_stylesheet[0]['style']['width'] = \
			f"mapData(num_edits, {network['user_min_edits']}, \
			{network['user_max_edits']}, 10, 60)"

		self.size_font_labels(network)


	def size_font_labels(self, network):
		if network['user_min_edits'] == network['user_max_edits']:
			super().size_font_labels(network)
			return

		self.cy_stylesheet[0]['style']['font-size'] = \
			f"mapData(num_edits, {network['user_min_edits']}, \
			{network['user_max_edits']}, 7, 18)"


	def color_edges(self, _):
		self.cy_stylesheet[1]['style']['line-color'] = \
			'mapData(w_time, 0, 2, #9E9E9E, #000000)'


	def set_edges_opacity(self, _):
		self.cy_stylesheet[1]['style']['opacity'] = \
			'mapData(w_time, 0, 2, 0.4, 1)'


	def size_edges(self, network):
		if network['edge_min_weight'] == network['edge_max_weight']:
			super().size_edges(network)
			return

		self.cy_stylesheet[1]['style']['width'] = \
			f"mapData(weight, {network['edge_min_weight']}, \
			{network['edge_max_weight']}, 1, 10)"


	def highlight_nodes(self, network, selc_nodes):
		self.size_nodes(network)
		self.color_edges(network)
		self.set_edges_opacity(network)
		self.size_edges(network)
		
		# the remaining nodes go backgroung
		self.cy_stylesheet[0]['style']['opacity'] = 0.3

		# selected nodes go foreground
		for node in selc_nodes:
			label = node['User']
			selector = f'node[label = "{label}"]'
			di_style = {
				'selector': selector,
				'style': self.HIGHLIGHT_NODE
			}
			self.cy_stylesheet.append(di_style)


	def all_transformations(self, network):
		self.color_nodes(network)
		self.size_nodes(network)
		self.color_edges(network)
		self.set_edges_opacity(network)
		self.size_edges(network)
