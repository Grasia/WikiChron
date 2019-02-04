#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   factory_stylesheet_decorator.py

   Descp:

   Created on: 04-feb-2019

   Copyright 2019 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

from ..networks.types.CoEditingNetwork import CoEditingNetwork
from .CoEditingCytoscapeDecorator import CoEditingCytoscapeDecorator


def construct_decorator_cytoscape_stylesheet(selected_network_code, stylesheet):

    if selected_network_code == CoEditingNetwork.CODE:
        return CoEditingCytoscapeDecorator(stylesheet)
    else:
        raise Exception("Something went bad. Missing network type selection.")

