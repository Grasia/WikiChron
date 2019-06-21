#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   metrics_generator.py

   Descp:

   Created on: 14-nov-2017

   Copyright 2017-2018 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

from .metric import Metric, MetricCategory
from . import stats

def generate_metrics():
    metrics = []
    # Pages
    metrics.append(Metric('pages_new', 'New pages', MetricCategory.PAGES, stats.pages_new, 'Number of new pages created per month'))
    metrics.append(Metric('pages_main_new', 'New articles', MetricCategory.PAGES, stats.pages_main_new, 'Number of new articles (main content) created per month'))
    metrics.append(Metric('pages_edited', 'Pages edited', MetricCategory.PAGES, stats.pages_edited, 'Number of different pages edited per month'))
    metrics.append(Metric('main_edited', 'Articles edited', MetricCategory.PAGES, stats.main_edited, 'Number of different articles edited per month'))
    metrics.append(Metric('pages_accum', 'Total pages', MetricCategory.PAGES, stats.pages_accum, 'Total of pages accumulated at every month'))
    metrics.append(Metric('pages_main_accum', 'Total articles', MetricCategory.PAGES, stats.pages_main_accum, 'Total of articles (main content) at every month'))

    # Editions
    metrics.append(Metric('edits', 'Edits in pages', MetricCategory.EDITIONS, stats.edits, 'Editions to any part of the wiki grouped by month'))
    metrics.append(Metric('edits_main_content', 'Edits in articles', MetricCategory.EDITIONS, stats.edits_main_content, 'Editions to articles (main content) per month'))
    metrics.append(Metric('edits_article_talk', 'Edits in articles talk', MetricCategory.EDITIONS, stats.edits_article_talk, 'Editions to article discussion pages'))
    metrics.append(Metric('edits_user_talk', 'Edits in user talk', MetricCategory.EDITIONS, stats.edits_user_talk, 'Editions to user discussion pages'))
    metrics.append(Metric('edits_accum', 'Total edits in pages', MetricCategory.EDITIONS, stats.edits_accum, 'Total editions to any part of the wiki accumulated at every month'))
    metrics.append(Metric('edits_main_content_accum', 'Total edits in articles', MetricCategory.EDITIONS, stats.edits_main_content_accum, 'Editions to articles accumulated at every month'))

    # Users
    metrics.append(Metric('users_new', 'New users', MetricCategory.USERS, stats.users_new, 'Users who have made at least one edition grouped by the month they did their first edit.'))
    metrics.append(Metric('users_new_registered', 'New registered users', MetricCategory.USERS, stats.users_new_registered, 'New users registration per month who have made at least one edition.'))
    metrics.append(Metric('users_new_anonymous', 'New anonymous users', MetricCategory.USERS, stats.users_new_anonymous, 'Anonymous users who made at least one edition grouped by the month they did their first edit. Anonymous are identified by their ip.'))
    metrics.append(Metric('users_accum', 'Total users', MetricCategory.USERS, stats.users_accum, 'Users who have made at least one edition accumulated at every month.'))
    metrics.append(Metric('users_registered_accum', 'Total registered users', MetricCategory.USERS, stats.users_registered_accum, 'Total registered users at every month. Note that users have to have made at least one edition and they have to be logged with their account when they did that edition.'))
    metrics.append(Metric('users_anonymous_accum', 'Total anonymous users', MetricCategory.USERS, stats.users_anonymous_accum, 'Anonymous users who have made at least one edition accumulated at every month. Anonymous are identified by their ip.'))
    metrics.append(Metric('users_active', 'Active users', MetricCategory.USERS, stats.users_active, 'Number of users who have made at least one contribution in a month.'))
    metrics.append(Metric('users_active_registered', 'Active registered users', MetricCategory.USERS, stats.users_registered_active, 'Number of registered users who have made at least one contribution in a month.'))
    metrics.append(Metric('users_active_anonymous', 'Active anonymous users', MetricCategory.USERS, stats.users_anonymous_active, 'Number of anonymous users who have made at least one contribution in a month.'))
    metrics.append(Metric('users_active_more_than_4', 'Active users with > 4 edits', MetricCategory.USERS, stats.users_active_more_than_4_editions, 'Active users who have made more than 4 editions in a month.'))
    metrics.append(Metric('users_active_more_than_24', 'Active users with > 24 edits', MetricCategory.USERS, stats.users_active_more_than_24_editions, 'Active users who have made more than 24 editions in a month.'))
    metrics.append(Metric('users_active_more_than_99', 'Active users with > 99 edits', MetricCategory.USERS, stats.users_active_more_than_99_editions, 'Active users who have made more than 99 editions in a month.'))

    # RATIO
    metrics.append(Metric('edits_per_users_monthly', 'Edits per users', MetricCategory.RATIOS, stats.edits_per_users_monthly, 'Number of edits for every month per number of active users that month'))
    metrics.append(Metric('edits_in_articles_per_users_monthly', 'Article edits per user', MetricCategory.RATIOS, stats.edits_in_articles_per_users_monthly, 'Number of edits in articles per number of users for each month'))
    metrics.append(Metric('edits_per_page_monthly', 'Edits per edited pages', MetricCategory.RATIOS, stats.edits_per_pages_monthly, 'Number of edits for every month per number of pages edited that month'))
    metrics.append(Metric('percentage_edits_by_anonymous_monthly', 'Anonymous edits (%)', MetricCategory.RATIOS, stats.percentage_edits_by_anonymous_monthly, 'Percentage of edits made by anonymous users of the total edits.'))
    metrics.append(Metric('edits_in_articles_per_users_accum', 'Total articles edits per user', MetricCategory.RATIOS, stats.edits_in_articles_per_users_accum, 'Number of total edits in articles per number of users until a given month'))
    metrics.append(Metric('edits_per_pages_accum', 'Total edits per page', MetricCategory.RATIOS, stats.edits_per_pages_accum, 'Number of total edits per number of total pages'))
    metrics.append(Metric('percentage_edits_by_anonymous_accum', 'Total anonymous edits (%)', MetricCategory.RATIOS, stats.percentage_edits_by_anonymous_accum, 'Percentage, per month, of edits made by anonymous users of the total edits.'))

    # RETENTION
    metrics.append(Metric('returning_new_editors', 'Returning new editors', MetricCategory.RETENTION, stats.returning_new_editors, "Number of new users who completes at least two edit sessions (60') within the first 30 days since registration. Based on a WMF's metric."))
    metrics.append(Metric('surviving_new_editors', 'Surviving new editors', MetricCategory.RETENTION, stats.surviving_new_editors, "Numer of new users who completes at least one edit within the first 30 days since registration and also completes another edit in the survival period, (i.e. the following 30 days). Based on a WMF's metric."))

    # DISTRIBUTION
    metrics.append(Metric('gini_accum', 'Gini coefficient', MetricCategory.DISTRIBUTION, stats.gini_accum, 'Gini coefficient (accumulated)'))
    metrics.append(Metric('ratio_10_90', '10:90 ratio', MetricCategory.DISTRIBUTION, stats.ratio_10_90, 'Contributions of the top ten percent more active users between the 90% percent less active'))
    metrics.append(Metric('ratio_percentiles_max_5', 'Participants prctl. top / 5', MetricCategory.DISTRIBUTION, stats.ratio_percentiles_max_5, 'Ratio between contributions of the top and the 5th top users'))
    metrics.append(Metric('ratio_percentiles_max_10', 'Participants prctl. top / 10', MetricCategory.DISTRIBUTION, stats.ratio_percentiles_max_10, 'Ratio between contributions of the top user and the 10th top user'))
    metrics.append(Metric('ratio_percentiles_max_20', 'Participants prctl. top / 20', MetricCategory.DISTRIBUTION, stats.ratio_percentiles_max_20, 'Ratio between contributions of the top user and the 20th top user'))
    metrics.append(Metric('ratio_percentiles_5_10', 'Participants prctl. 5 / 10', MetricCategory.DISTRIBUTION, stats.ratio_percentiles_5_10, 'Ratio between contributions of the 5th user and the 10th top user'))
    metrics.append(Metric('ratio_percentiles_10_20', 'Participants prctl. 10 / 20', MetricCategory.DISTRIBUTION, stats.ratio_percentiles_10_20, 'Ratio between contributions of the 10th user and the 20th top user'))

    # keep this order when plotting graphs inserting 'index_' at the beginning
    #  for every metric code.
    # NOTE: Possibly, It'll be changed in the future by an specifc attr: "order"
    #  in the GUI side, in order to be able to reorder the plots.
    for idx in range(len(metrics)):
        metrics[idx].code = "{idx}_{code}".format(idx=idx, code=metrics[idx].code)

    return metrics

def generate_dict_metrics(list_of_metrics):
    metrics = {}

    for metric in list_of_metrics:
        metrics[metric.code] = metric

    return metrics


def generate_dict_metrics_by_category(list_of_metrics):
    # group metrics in a dict w/ key: category, value: [metrics]
    metrics_by_category = {}
    for metric in list_of_metrics:
        if metric.category not in metrics_by_category:
            metrics_by_category[metric.category] = [metric]
        else:
            metrics_by_category[metric.category].append(metric)

    return metrics_by_category

