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
    metrics.append(Metric('pages_edited', 'Pages edited monthly', MetricCategory.PAGES, stats.pages_edited, 'Number of different pages edited per month'))
    metrics.append(Metric('main_edited', 'Articles edited monthly', MetricCategory.PAGES, stats.main_edited, 'Number of different articles edited per month'))

    # Editions
    metrics.append(Metric('edits', 'Global edits monthly', MetricCategory.EDITIONS, stats.edits, 'Editions to any part of the wiki grouped by month'))
    metrics.append(Metric('edits_accum', 'Global edits (accumulated)', MetricCategory.EDITIONS, stats.edits_accum, 'Total editions to any part of the wiki accumulated at every month'))
    metrics.append(Metric('edits_main_content', 'Edits in articles', MetricCategory.EDITIONS, stats.edits_main_content, 'Editions to articles (main content) per month'))
    metrics.append(Metric('edits_main_content_accum', 'Edits in articles (accumulated)', MetricCategory.EDITIONS, stats.edits_main_content_accum, 'Editions to articles accumulated at every month'))
    metrics.append(Metric('edits_article_talk', 'Edits in articles talk', MetricCategory.EDITIONS, stats.edits_article_talk, 'Editions to article discussion pages'))
    metrics.append(Metric('edits_user_talk', 'Edits in user talk', MetricCategory.EDITIONS, stats.edits_user_talk, 'Editions to user discussion pages'))

    # Users
    metrics.append(Metric('users_active', 'Monthly active users', MetricCategory.USERS, stats.users_active, 'Number of users who have made at least one contribution for each month.'))
    metrics.append(Metric('users_new', 'Monthly new users', MetricCategory.USERS, stats.users_new, 'Users who have made at least one edition grouped by the month they did their first edit.'))
    metrics.append(Metric('users_accum', 'Total users (accumulated)', MetricCategory.USERS, stats.users_accum, 'Users who have made at least one edition accumulated at every month.'))
    metrics.append(Metric('users_new_anonymous', 'Monthly anonymous users.', MetricCategory.USERS, stats.users_new_anonymous, 'Anonymous users who made at least one edition grouped by the month they did their first edit. Anonymous are identified by their ip.'))
    metrics.append(Metric('users_anonymous_accum', 'Total anonymous users (accumulated)', MetricCategory.USERS, stats.users_anonymous_accum, 'Anonymous users who have made at least one edition accumulated at every month. Anonymous are identified by their ip.'))
    metrics.append(Metric('users_new_registered', 'Monthly new registered users', MetricCategory.USERS, stats.users_new_registered, 'New users registration per month who have made at least one edition.'))
    metrics.append(Metric('users_registered_accum', 'Total registered users (accumulated)', MetricCategory.USERS, stats.users_registered_accum, 'Total registered users at every month. Note that users have to have made at least one edition and they have to be logged with their account when they did that edition.'))

    # RATIO
    metrics.append(Metric('edits_per_users_accum', 'Edits per users (accumulated)', MetricCategory.RATIOS, stats.edits_per_users_accum, 'Number of total edits per number of users'))
    metrics.append(Metric('edits_per_users_monthly', 'Edits per users (monthly)', MetricCategory.RATIOS, stats.edits_per_users_monthly, 'Number of edits for every month per number of active users that month'))
    metrics.append(Metric('edits_per_pages_accum', 'Edits per pages (accumulated)', MetricCategory.RATIOS, stats.edits_per_pages_accum, 'Number of total edits per number of total pages'))
    metrics.append(Metric('edits_per_page_monthly', 'Edits per pages edited (monthly)', MetricCategory.RATIOS, stats.edits_per_pages_monthly, 'Number of edits for every month per number of pages edited that month'))

    # INEQUALITY
    metrics.append(Metric('gini_accum', 'Gini (accumulated)', MetricCategory.DISTRIBUTION, stats.gini_accum, ''))
    metrics.append(Metric('ratio_percentiles_max_5_old', 'Percentil MAX / 5', MetricCategory.DISTRIBUTION, stats.ratio_percentiles_max_5_old, ''))

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

