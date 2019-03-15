#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   __init__.py

   Defines metrics package and init public list: available_metrics.

   Created on: 15-nov-2017

   Copyright 2017-2018 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

from .metrics_generator import generate_metrics, generate_dict_metrics

print('Generating available metrics...')
available_metrics = generate_metrics()
metrics_dict = generate_dict_metrics(available_metrics)
