#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   metrics_generator.py

   Descp:

   Created on: 14-nov-2017
   Copyright 2017-2018 Youssef 'FRYoussef' El Faqir El Rhazoui <f.r.youssef@hotmail.com>
   Copyright 2017-2018 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

from .types.CoEditingNetwork import CoEditingNetwork

def create_available_networks():
	networks = []
	networks.append(CoEditingNetwork())
	return networks

def factory_network(selected_network_code):
    if selected_network_code:
        return CoEditingNetwork()
    else:
        raise Exception("Something went bad. Missing network type selection.")