#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   metrics_generator.py

   Descp:

   Created on: 14-nov-2017
   Copyright 2017-2019 Youssef 'FRYoussef' El Faqir El Rhazoui <f.r.youssef@hotmail.com>
   Copyright 2017-2019 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

from .CoEditingNetwork import CoEditingNetwork
from .TalkPagesNetwork import TalkPagesNetwork

def create_available_networks():
    networks = [CoEditingNetwork, TalkPagesNetwork]
    return networks

def factory_network(network_code):
    if network_code == CoEditingNetwork.CODE:
        return CoEditingNetwork()
    elif network_code == TalkPagesNetwork.CODE:
        return TalkPagesNetwork()
    else:
        raise Exception("Something went bad. Missing network type selection.")


def get_user_info(network_code):
    if network_code == CoEditingNetwork.CODE:
        return CoEditingNetwork.get_user_info()
    elif network_code == TalkPagesNetwork.CODE:
        return TalkPagesNetwork.get_user_info()
    else:
        raise Exception("Something went bad. Missing network type selection.")


def get_available_metrics(network_code):
    if network_code == CoEditingNetwork.CODE:
        return CoEditingNetwork.get_available_metrics()
    elif network_code == TalkPagesNetwork.CODE:
        return TalkPagesNetwork.get_available_metrics()
    else:
        raise Exception("Something went bad. Missing network type selection.")


def get_secondary_metrics(network_code):
    if network_code == CoEditingNetwork.CODE:
        return CoEditingNetwork.get_secondary_metrics()
    elif network_code == TalkPagesNetwork.CODE:
        return TalkPagesNetwork.get_secondary_metrics()
    else:
        raise Exception("Something went bad. Missing network type selection.")