#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   metrics_generator.py

   Descp:

   Created on: 14-nov-2017

   Copyright 2017 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

from .metric import Metric, MetricCategory
from . import stats

def generate_metrics():
    metrics = []
    # Editions
    metrics.append(Metric('edits_monthly', 'Monthly edits', MetricCategory.EDITIONS, stats.edits_monthly))

    # Users
    metrics.append(Metric('users_new', 'Monthly new users', MetricCategory.USERS, stats.users_new))

    return metrics

def main():
    print (generate_metrics())
    return

if __name__ == '__main__':
    main()

