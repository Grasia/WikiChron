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
    metrics.append(Metric('edits_monthly', 'Monthly edits', MetricCategory.EDITIONS, stats.edits_monthly, 'Editions to any part of the wiki grouped by month'))

    # Users
    metrics.append(Metric('users_new', 'Monthly new users', MetricCategory.USERS, stats.users_new, 'Users who have made at least one edition grouped by the month they did her first edit.'))

    return metrics

def generate_dict_metrics(list_of_metrics):
    metrics = {}

    for metric in list_of_metrics:
        metrics[metric.code] = metric

    return metrics


def main():
    print (generate_metrics())
    return

if __name__ == '__main__':
    main()

