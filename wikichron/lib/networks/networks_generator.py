#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   metrics_generator.py

   Descp:

   Created on: 14-nov-2017

   Copyright 2017-2018 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

from .types.CoEditingNetwork import CoEditingNetwork

def create_available_networks():
	networks = []
	networks.append(CoEditingNetwork())
	return networks