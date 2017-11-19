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
    # Pages
    metrics.append(Metric('pages_new', 'New pages monthly', MetricCategory.PAGES, stats.pages_new, 'Number of new pages created per month'))
    metrics.append(Metric('pages_accum', 'New pages (accumulated)', MetricCategory.PAGES, stats.pages_accum, 'Total of pages accumulated at every month'))
    metrics.append(Metric('pages_main_new', 'New articles monthly', MetricCategory.PAGES, stats.pages_main_new, 'Number of new articles (main content) created per month'))
    metrics.append(Metric('pages_main_accum', 'New articles (accumulated)', MetricCategory.PAGES, stats.pages_main_accum, 'Total of articles (main content) at every month'))
    metrics.append(Metric('pages_edited', 'Pages edited monthly', MetricCategory.PAGES, stats.pages_edited, 'Number of different pages with edits per month'))

    # Editions
    metrics.append(Metric('edits', 'Global edits monthly', MetricCategory.EDITIONS, stats.edits, 'Editions to any part of the wiki grouped by month'))
    metrics.append(Metric('edits_accum', 'Global edits (accumulated)', MetricCategory.EDITIONS, stats.edits_accum, 'Total editions to any part of the wiki accumulated at every month'))
    metrics.append(Metric('edits_main_content', 'Edits in articles', MetricCategory.EDITIONS, stats.edits_main_content, 'Editions to articles (main content) per month'))
    metrics.append(Metric('edits_main_content_accum', 'Edits in articles (accumulated)', MetricCategory.EDITIONS, stats.edits_main_content_accum, 'Editions to articles accumulated at every month'))
    metrics.append(Metric('edits_article_talk', 'Edits in articles talk', MetricCategory.EDITIONS, stats.edits_article_talk, 'Editions to article discussion pages'))
    metrics.append(Metric('edits_user_talk', 'Edits in user talk', MetricCategory.EDITIONS, stats.edits_user_talk, 'Editions to user discussion pages'))

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

