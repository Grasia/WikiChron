"""
   CytoscapeStylesheet.py

   Descp: A class to warp the cytoscape stylesheet

   Created on: 15/03/2019

   Copyright 2019 Youssef 'FRYoussef' El Faqir el Rhazoui <f.r.youssef@hotmail.com>
"""

class CytoscapeStylesheet():

	HIGHLIGHT_NODE = {
			"background-color": "#B10DC9",
			"border-color": "black",
			"border-width": 2,
			"border-opacity": 1,
			"opacity": 1,
			"label": "data(label)",
			"text-opacity": 1,
			"z-index": 9999
		}

	def __init__(self, cy_stylesheet = []):
		if not cy_stylesheet:
			self.cy_stylesheet = self.make_basic_stylesheet()
		else:
			self.cy_stylesheet = cy_stylesheet


	def color_nodes(self, network):
		if network['first_entry'] == network['last_entry']:
			self.cy_stylesheet[0]['style']['background-color'] = '#0D47A1'
			return

		self.cy_stylesheet[0]['style']['background-color'] = \
			f"mapData(first_edit, {network['first_entry']}, \
			{network['last_entry']}, #64B5F6, #0D47A1)"


	def color_nodes_by_cluster(self):
		self.cy_stylesheet[0]['style']['background-color'] = 'data(cluster_color)'


	def size_nodes_default(self):
		self.cy_stylesheet[0]['style']['height'] = '30'
		self.cy_stylesheet[0]['style']['width'] = '30'
		self.size_font_labels_default()

	def size_nodes(self, network):
		if not all(k in network for k in ('min_node_size', 'max_node_size')):
			self.size_nodes_default()
			return

		if network['min_node_size'] == network['max_node_size']:
			self.size_nodes_default()
			return

		self.cy_stylesheet[0]['style']['height'] = \
			f"mapData(num_edits, {network['min_node_size']}, \
			{network['max_node_size']}, 10, 60)"

		self.cy_stylesheet[0]['style']['width'] = \
			f"mapData(num_edits, {network['min_node_size']}, \
			{network['max_node_size']}, 10, 60)"

		self.size_font_labels(network)


	def size_font_labels_default(self):	
		self.cy_stylesheet[0]['style']['font-size'] = '12'


	def size_font_labels(self, network):
		if not all(k in network for k in ('min_node_size', 'max_node_size')):
			self.size_font_labels_default()
			return

		if network['min_node_size'] == network['max_node_size']:
			self.size_font_labels_default()
			return

		self.cy_stylesheet[0]['style']['font-size'] = \
			f"mapData(num_edits, {network['min_node_size']}, \
			{network['max_node_size']}, 7, 18)"


	# def color_edges(self, _):
	# 	self.cy_stylesheet[1]['style']['line-color'] = \
	# 		'mapData(w_time, 0, 2, #9E9E9E, #000000)'
	def color_edges(self, _):
		self.cy_stylesheet[1]['style']['line-color'] = '#000000'


	# def set_edges_opacity(self, _):
	# 	self.cy_stylesheet[1]['style']['opacity'] = \
	# 		'mapData(w_time, 0, 2, 0.4, 1)'
	def set_edges_opacity(self, _):
		self.cy_stylesheet[1]['style']['opacity'] = '1'


	def size_edges_default(self):
		self.cy_stylesheet[1]['style']['width'] = '1'


	def size_edges(self, network):
		if not all(k in network for k in ('min_edge_size', 'max_edge_size')):
			self.size_edges_default()
			return

		if network['min_edge_size'] == network['max_edge_size']:
			self.size_edges_default()
			return

		self.cy_stylesheet[1]['style']['width'] = \
			f"mapData(weight, {network['min_edge_size']}, \
			{network['max_edge_size']}, 1, 10)"


	def set_label(self, text):
		content = f'data({text})' if text else ''
		self.cy_stylesheet[0]['style']['content'] = content


	def all_transformations(self, network):
		self.color_nodes(network)
		self.size_nodes(network)
		self.color_edges(network)
		self.set_edges_opacity(network)
		self.size_edges(network)


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


	@classmethod
	def make_basic_stylesheet(cls):
		return [{
                'selector': 'node',
                'style': {
                    'content': '',
                    'text-halign': 'center',
                    'text-valign': 'top',
                    'text-background-color': '#FFFFFF',
                    'text-background-opacity': '1',
                    'font-size': '12',
                    'background-color': '#0D47A1',
                    'height': '30',
                    'width': '30'
                }
            },
            {
                'selector': 'edge',
                'style': {
                    "width": 1,
                    'opacity': '1',
                    'line-color': "#000000",
                }
            }]