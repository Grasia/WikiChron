#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   metrics_generator.py

   Descp:

   Created on: 14-nov-2017

   Copyright 2017-2018 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

from .types.NetworkType import Network
from .types import co_editing_network

def create_available_networks():
    networks = [Network('co_editing_network', 'Co-editing', co_editing_network.generate_network)]
    return networks
