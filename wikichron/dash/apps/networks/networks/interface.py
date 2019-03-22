#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   interface.py

   Descp. Interface between lib backend and the Dash app

   Created on: 14-nov-2017

   Copyright 2018-2019 Youssef 'FRYoussef' El Faqir El Rhazoui <f.r.youssef@hotmail.com>
"""

from .models import available_networks as _available_networks
from .models.networks_generator import factory_network as _factory_network


def get_available_networks():
    """ Return a list of the currently available networks. """
    return _available_networks


def factory_network(selected_network_code, wiki):
    return _factory_network(selected_network_code, wiki)
