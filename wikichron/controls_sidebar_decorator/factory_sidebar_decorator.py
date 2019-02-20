"""
   factory_sidebar_decorator.py

   Descp:

   Created on: 08-feb-2019

   Copyright 2019 Youssef 'FRYoussef' El Faqir el Rhazoui <f.r.youssef@hotmail.com>
"""

from lib.networks.types.CoEditingNetwork import CoEditingNetwork
from .CoEditingControlsSidebarDecorator import CoEditingControlsSidebarDecorator


def factory_sidebar_decorator(selected_network_code, sidebar):
	if selected_network_code == CoEditingNetwork.CODE:
		return CoEditingControlsSidebarDecorator(sidebar)
	else:
		raise Exception("Something went bad. Missing network type selection.")


def bind_controls_sidebar_callbacks(selected_network_code, app):
	if selected_network_code == CoEditingNetwork.CODE:
		CoEditingControlsSidebarDecorator.bind_callbacks(app = app)
	else:
		raise Exception("Something went bad. Missing network type selection.")