#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   metrics_generator.py

   Descp:

   Created on: 14-nov-2017
   Copyright 2017-2019 Youssef 'FRYoussef' El Faqir El Rhazoui <f.r.youssef@hotmail.com>
"""

from .BaseNetwork import BaseNetwork
from .CoEditingNetwork import CoEditingNetwork
from .TalkPagesNetwork import TalkPagesNetwork
from .UserTalkNetwork import UserTalkNetwork


def create_available_networks():
    networks = [CoEditingNetwork, TalkPagesNetwork, UserTalkNetwork]
    return networks


def factory_network(network_code, alias):
    if network_code == CoEditingNetwork.CODE:
        return CoEditingNetwork(alias=alias)
    elif network_code == TalkPagesNetwork.CODE:
        return TalkPagesNetwork(alias=alias)
    elif network_code == UserTalkNetwork.CODE:
        return UserTalkNetwork(alias=alias)
    else:
        raise Exception("Something went bad. Missing network type selection.")


def get_user_info(network_code):
    if network_code == CoEditingNetwork.CODE:
        return CoEditingNetwork.get_user_info()
    elif network_code == TalkPagesNetwork.CODE:
        return TalkPagesNetwork.get_user_info()
    elif network_code == UserTalkNetwork.CODE:
        return UserTalkNetwork.get_user_info()
    else:
        raise Exception("Something went bad. Missing network type selection.")


def get_node_name(network_code):
    if network_code == CoEditingNetwork.CODE:
        return CoEditingNetwork.get_node_name()
    elif network_code == TalkPagesNetwork.CODE:
        return TalkPagesNetwork.get_node_name()
    elif network_code == UserTalkNetwork.CODE:
        return UserTalkNetwork.get_node_name()
    else:
        raise Exception("Something went bad. Missing network type selection.")


def get_metrics_to_plot(network_code):
    if network_code == CoEditingNetwork.CODE:
        return CoEditingNetwork.get_metrics_to_plot()
    elif network_code == TalkPagesNetwork.CODE:
        return TalkPagesNetwork.get_metrics_to_plot()
    elif network_code == UserTalkNetwork.CODE:
        return UserTalkNetwork.get_metrics_to_plot()
    else:
        raise Exception("Something went bad. Missing network type selection.")


def get_node_metrics(network_code):
    if network_code == CoEditingNetwork.CODE:
        return CoEditingNetwork.get_node_metrics()
    elif network_code == TalkPagesNetwork.CODE:
        return TalkPagesNetwork.get_node_metrics()
    elif network_code == UserTalkNetwork.CODE:
        return UserTalkNetwork.get_node_metrics()
    else:
        raise Exception("Something went bad. Missing network type selection.")


def get_metrics_to_show(network_code):
    if network_code == CoEditingNetwork.CODE:
        return CoEditingNetwork.get_metrics_to_show()
    elif network_code == TalkPagesNetwork.CODE:
        return TalkPagesNetwork.get_metrics_to_show()
    elif network_code == UserTalkNetwork.CODE:
        return UserTalkNetwork.get_metrics_to_show()
    else:
        raise Exception("Something went bad. Missing network type selection.")


def is_directed(network_code) -> bool:
    if network_code == CoEditingNetwork.CODE:
        return CoEditingNetwork.is_directed()
    elif network_code == TalkPagesNetwork.CODE:
        return TalkPagesNetwork.is_directed()
    elif network_code == UserTalkNetwork.CODE:
        return UserTalkNetwork.is_directed()
    else:
        raise Exception("Something went bad. Missing network type selection.")


def get_metric_header(network_code, metric) -> bool:
    if network_code == CoEditingNetwork.CODE:
        return CoEditingNetwork.get_metric_header(metric)
    elif network_code == TalkPagesNetwork.CODE:
        return TalkPagesNetwork.get_metric_header(metric)
    elif network_code == UserTalkNetwork.CODE:
        return UserTalkNetwork.get_metric_header(metric)
    else:
        raise Exception("Something went bad. Missing network type selection.")


def get_network_stats(network_code: str) -> dict:
    if network_code == CoEditingNetwork.CODE:
        return CoEditingNetwork.get_network_stats()
    elif network_code == TalkPagesNetwork.CODE:
        return TalkPagesNetwork.get_network_stats()
    elif network_code == UserTalkNetwork.CODE:
        return UserTalkNetwork.get_network_stats()
    else:
        raise Exception("Something went bad. Missing network type selection.")