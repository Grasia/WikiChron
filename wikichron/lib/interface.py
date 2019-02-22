#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   interface.py

   Descp. Interface between lib backend and the Dash app

   Created on: 14-nov-2017

   Copyright 2017-2019 Youssef 'FRYoussef' El Faqir El Rhazoui <f.r.youssef@hotmail.com>
   Copyright 2017-2019 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

from .networks import available_networks as _available_networks
from .networks.networks_generator import factory_network as _factory_network


def get_available_networks():
    """ Return a list of the currently available networks. """
    return _available_networks


def factory_network(selected_network_code):
    return _factory_network(selected_network_code)


def get_network_from_bin(name, network_t):
    """
    Find and read a network from a bin file

    Parameters:
      - name: the network name
      - network_t: the network type

    Return:
      - 0 if the file doesn't exist
      - An network_t type instance if it exist

    Raise Exception:
      - network_t is not avaliable
    """
