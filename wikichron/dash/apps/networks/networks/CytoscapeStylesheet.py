"""
   CytoscapeStylesheet.py

   Descp: A class to warp the cytoscape stylesheet

   Created on: 15/03/2019

   Copyright 2019 Youssef 'FRYoussef' El Faqir el Rhazoui <f.r.youssef@hotmail.com>
"""

class CytoscapeStylesheet():

	N_DEFAULT_COLOR = '#78909C'
	N_MIN_COLOR = '#F3E5F5'
	N_MAX_COLOR = '#1A237E'
	N_DEFAULT_SIZE = '10'
	N_MIN_SIZE = '10'
	N_MAX_SIZE = '60'
	N_DEFAULT_FONT = '12'
	N_MIN_FONT = '7'
	N_MAX_FONT = '18'
	E_DEFAULT_COLOR = '#000000'
	E_ARROW_COLOR = '#3E2723'
	E_MIN_COLOR = ''
	E_MAX_COLOR = ''
	E_DEFAULT_SIZE = '1'
	E_MIN_SIZE = '1'
	E_MAX_SIZE = '10'
	E_DEFAULT_OPACITY = '1'
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
	
	EDGE_LABEL = {
		"label": "data(weight)",
		"z-index": 9999,
		"text-opacity": 1,
		"opacity": 1,
		'text-valign': 'top',
		'text-background-color': '#FFFFFF',
		'text-background-opacity': '1'
	}


	def __init__(self, directed = False, cy_stylesheet = []):
		if not cy_stylesheet:
			self.cy_stylesheet = self.make_basic_stylesheet()
		else:
			self.cy_stylesheet = cy_stylesheet
		if directed:
			self.add_directed_edges()
	

	def add_directed_edges(self):
		self.cy_stylesheet[1]['style']['curve-style'] = 'bezier'
		self.cy_stylesheet[1]['style']['target-arrow-shape'] = 'triangle'
		self.cy_stylesheet[1]['style']['target-arrow-color'] = self.E_ARROW_COLOR


	def color_nodes_default(self, color):
		self.cy_stylesheet[0]['style']['background-color'] = color


	def color_nodes(self, network, metric):
		if not metric or not all(k in metric for k in ('max', 'min', 'key')):
			self.color_nodes_default(self.N_DEFAULT_COLOR)
			return

		if network[metric['max']] == network[metric['min']]:
			self.color_nodes_default(self.N_MIN_COLOR)
			return

		key = metric['log'] if 'log' in metric else metric['key']

		self.cy_stylesheet[0]['style']['background-color'] = \
			f"mapData({key}, {network[metric['min']]}, \
			{network[metric['max']]}, {self.N_MIN_COLOR}, {self.N_MAX_COLOR})"


	def color_nodes_by_cluster(self):
		self.cy_stylesheet[0]['style']['background-color'] = 'data(cluster_color)'


	def size_nodes_default(self):
		self.cy_stylesheet[0]['style']['height'] = self.N_DEFAULT_SIZE
		self.cy_stylesheet[0]['style']['width'] = self.N_DEFAULT_SIZE
		self.size_font_labels_default()


	def size_nodes(self, network, metric):
		if not metric or not all(k in metric for k in ('min', 'max', 'key')):
			self.size_nodes_default()
			return

		if network[metric['max']] == network[metric['min']]:
			self.size_nodes_default()
			return
		
		key = metric['log'] if 'log' in metric else metric['key']

		self.cy_stylesheet[0]['style']['height'] = f"mapData({key}, {network[metric['min']]}, \
			{network[metric['max']]}, {self.N_MIN_SIZE}, {self.N_MAX_SIZE})"

		self.cy_stylesheet[0]['style']['width'] = f"mapData({key}, {network[metric['min']]}, \
			{network[metric['max']]}, {self.N_MIN_SIZE}, {self.N_MAX_SIZE})"

		self.size_font_labels(network, metric)


	def size_font_labels_default(self):	
		self.cy_stylesheet[0]['style']['font-size'] = self.N_DEFAULT_FONT


	def size_font_labels(self, network, metric):
		if not metric or not all(k in metric for k in ('min', 'max', 'key')):
			self.size_font_labels_default()
			return

		if network[metric['max']] == network[metric['min']]:
			self.size_font_labels_default()
			return

		key = metric['log'] if 'log' in metric else metric['key']

		self.cy_stylesheet[0]['style']['font-size'] = f"mapData({key}, {network[metric['min']]}, \
			{network[metric['max']]}, {self.N_MIN_FONT}, {self.N_MAX_FONT})"


	def color_edges(self, _):
		self.cy_stylesheet[1]['style']['line-color'] = self.E_DEFAULT_COLOR


	def set_edges_opacity(self, _):
		self.cy_stylesheet[1]['style']['opacity'] = self.E_DEFAULT_OPACITY


	def size_edges_default(self):
		self.cy_stylesheet[1]['style']['width'] = self.E_DEFAULT_SIZE


	def size_edges(self, network):
		if not all(k in network for k in ('min_weight', 'max_weight')):
			self.size_edges_default()
			return

		if network['min_weight'] == network['max_weight']:
			self.size_edges_default()
			return

		self.cy_stylesheet[1]['style']['width'] = \
			f"mapData(weight, {network['min_weight']}, \
			{network['max_weight']}, {self.E_MIN_SIZE}, {self.E_MAX_SIZE})"


	def set_label(self, text):
		content = f'data({text})' if text else ''
		self.cy_stylesheet[0]['style']['content'] = content


	def set_edge_label(self, edge_id):
		if not edge_id:
			return

		selector = f'edge[id = "{edge_id}"]'
		di_style = {
			'selector': selector,
			'style': self.EDGE_LABEL
		}
		self.cy_stylesheet.append(di_style)


	def all_transformations(self, network, metric_color, metric_size):
		self.color_nodes(network, metric_color)
		self.size_nodes(network, metric_size)
		self.color_edges(network)
		self.set_edges_opacity(network)
		self.size_edges(network)
		self.set_edge_label('')


	def highlight_nodes(self, network, selc_nodes, metric_size):
		self.size_nodes(network, metric_size)
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
                    'font-size': cls.N_DEFAULT_FONT,
                    'background-color': cls.N_DEFAULT_COLOR,
                    'height': cls.N_DEFAULT_SIZE,
                    'width': cls.N_DEFAULT_SIZE,
					'border-color': 'black',
					'border-width': 1,
					'border-opacity': 1,
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'width': cls.E_DEFAULT_SIZE,
                    'opacity': cls.E_DEFAULT_OPACITY,
                    'line-color': cls.E_DEFAULT_COLOR
                }
            }]