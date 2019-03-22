#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   __init__.py

   Defines metrics package and init public list: available_metrics.

   Created on: 15-nov-2017

   Copyright 2018-2019 Youssef 'FRYoussef' El Faqir El Rhazoui <f.r.youssef@hotmail.com>
"""

from .networks_generator import create_available_networks

print('Generating available networks...')
available_networks = create_available_networks()
print('This is the list of types of networks available currently:')
for nw in available_networks:
    print(f"\t * {nw.NAME}");
