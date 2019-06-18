#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   metrics_generator.py

   Descp:

   Created on: 14-nov-2017

   Copyright 2017-2019 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

from .metric import Metric, MetricCategory
from . import classic_stats
from . import monowiki_stats

def generate_classic_metrics():
    metrics = []

    # Pages
    metrics.append(Metric('pages_new', 'New pages', MetricCategory.PAGES, classic_stats.pages_new, 'Number of new pages created per month'))
    metrics.append(Metric('pages_main_new', 'New articles', MetricCategory.PAGES, classic_stats.pages_main_new, 'Number of new articles (main content) created per month'))
    metrics.append(Metric('pages_edited', 'Pages edited', MetricCategory.PAGES, classic_stats.pages_edited, 'Number of different pages edited per month'))
    metrics.append(Metric('main_edited', 'Articles edited', MetricCategory.PAGES, classic_stats.main_edited, 'Number of different articles edited per month'))
    metrics.append(Metric('pages_accum', 'Total pages', MetricCategory.PAGES, classic_stats.pages_accum, 'Total of pages accumulated at every month'))
    metrics.append(Metric('pages_main_accum', 'Total articles', MetricCategory.PAGES, classic_stats.pages_main_accum, 'Total of articles (main content) at every month'))

    # Editions
    metrics.append(Metric('edits', 'Edits in pages', MetricCategory.EDITIONS, classic_stats.edits, 'Editions to any part of the wiki grouped by month'))
    metrics.append(Metric('edits_main_content', 'Edits in articles', MetricCategory.EDITIONS, classic_stats.edits_main_content, 'Editions to articles (main content) per month'))
    metrics.append(Metric('edits_article_talk', 'Edits in articles talk', MetricCategory.EDITIONS, classic_stats.edits_article_talk, 'Editions to article discussion pages'))
    metrics.append(Metric('edits_user_talk', 'Edits in user talk', MetricCategory.EDITIONS, classic_stats.edits_user_talk, 'Editions to user discussion pages'))
    metrics.append(Metric('edits_accum', 'Total edits in pages', MetricCategory.EDITIONS, classic_stats.edits_accum, 'Total editions to any part of the wiki accumulated at every month'))
    metrics.append(Metric('edits_main_content_accum', 'Total edits in articles', MetricCategory.EDITIONS, classic_stats.edits_main_content_accum, 'Editions to articles accumulated at every month'))

    # Users
    metrics.append(Metric('users_new', 'New users', MetricCategory.USERS, classic_stats.users_new, 'Users who have made at least one edition grouped by the month they did their first edit.'))
    metrics.append(Metric('users_new_registered', 'New registered users', MetricCategory.USERS, classic_stats.users_new_registered, 'New users registration per month who have made at least one edition.'))
    metrics.append(Metric('users_new_anonymous', 'New anonymous users', MetricCategory.USERS, classic_stats.users_new_anonymous, 'Anonymous users who made at least one edition grouped by the month they did their first edit. Anonymous are identified by their ip.'))
    metrics.append(Metric('users_accum', 'Total users', MetricCategory.USERS, classic_stats.users_accum, 'Users who have made at least one edition accumulated at every month.'))
    metrics.append(Metric('users_registered_accum', 'Total registered users', MetricCategory.USERS, classic_stats.users_registered_accum, 'Total registered users at every month. Note that users have to have made at least one edition and they have to be logged with their account when they did that edition.'))
    metrics.append(Metric('users_anonymous_accum', 'Total anonymous users', MetricCategory.USERS, classic_stats.users_anonymous_accum, 'Anonymous users who have made at least one edition accumulated at every month. Anonymous are identified by their ip.'))
    metrics.append(Metric('users_active', 'Active users', MetricCategory.USERS, classic_stats.users_active, 'Number of users who have made at least one contribution in a month.'))
    metrics.append(Metric('users_active_registered', 'Active registered users', MetricCategory.USERS, classic_stats.users_registered_active, 'Number of registered users who have made at least one contribution in a month.'))
    metrics.append(Metric('users_active_anonymous', 'Active anonymous users', MetricCategory.USERS, classic_stats.users_anonymous_active, 'Number of anonymous users who have made at least one contribution in a month.'))
    metrics.append(Metric('users_active_more_than_4', 'Active users with > 4 edits', MetricCategory.USERS, classic_stats.users_active_more_than_4_editions, 'Active users who have made more than 4 editions in a month.'))
    metrics.append(Metric('users_active_more_than_24', 'Active users with > 24 edits', MetricCategory.USERS, classic_stats.users_active_more_than_24_editions, 'Active users who have made more than 24 editions in a month.'))
    metrics.append(Metric('users_active_more_than_99', 'Active users with > 99 edits', MetricCategory.USERS, classic_stats.users_active_more_than_99_editions, 'Active users who have made more than 99 editions in a month.'))

    # RATIO
    metrics.append(Metric('edits_per_users_monthly', 'Edits per users', MetricCategory.RATIOS, classic_stats.edits_per_users_monthly, 'Number of edits for every month per number of active users that month'))
    metrics.append(Metric('edits_in_articles_per_users_monthly', 'Article edits per user', MetricCategory.RATIOS, classic_stats.edits_in_articles_per_users_monthly, 'Number of edits in articles per number of users for each month'))
    metrics.append(Metric('edits_per_page_monthly', 'Edits per edited pages', MetricCategory.RATIOS, classic_stats.edits_per_pages_monthly, 'Number of edits for every month per number of pages edited that month'))
    metrics.append(Metric('percentage_edits_by_anonymous_monthly', 'Anonymous edits (%)', MetricCategory.RATIOS, classic_stats.percentage_edits_by_anonymous_monthly, 'Percentage of edits made by anonymous users of the total edits.'))
    metrics.append(Metric('edits_in_articles_per_users_accum', 'Total articles edits per user', MetricCategory.RATIOS, classic_stats.edits_in_articles_per_users_accum, 'Number of total edits in articles per number of users until a given month'))
    metrics.append(Metric('edits_per_pages_accum', 'Total edits per page', MetricCategory.RATIOS, classic_stats.edits_per_pages_accum, 'Number of total edits per number of total pages'))
    metrics.append(Metric('percentage_edits_by_anonymous_accum', 'Total anonymous edits (%)', MetricCategory.RATIOS, classic_stats.percentage_edits_by_anonymous_accum, 'Percentage, per month, of edits made by anonymous users of the total edits.'))

    # DISTRIBUTION
    metrics.append(Metric('gini_accum', 'Gini coefficient', MetricCategory.DISTRIBUTION, classic_stats.gini_accum, 'Gini coefficient (accumulated)'))
    metrics.append(Metric('ratio_10_90', '10:90 ratio', MetricCategory.DISTRIBUTION, classic_stats.ratio_10_90, 'Contributions of the top ten percent more active users between the 90% percent less active'))
    metrics.append(Metric('ratio_percentiles_max_5', 'Participants prctl. top / 5', MetricCategory.DISTRIBUTION, classic_stats.ratio_percentiles_max_5, 'Ratio between contributions of the top and the 5th top users'))
    metrics.append(Metric('ratio_percentiles_max_10', 'Participants prctl. top / 10', MetricCategory.DISTRIBUTION, classic_stats.ratio_percentiles_max_10, 'Ratio between contributions of the top user and the 10th top user'))
    metrics.append(Metric('ratio_percentiles_max_20', 'Participants prctl. top / 20', MetricCategory.DISTRIBUTION, classic_stats.ratio_percentiles_max_20, 'Ratio between contributions of the top user and the 20th top user'))
    metrics.append(Metric('ratio_percentiles_5_10', 'Participants prctl. 5 / 10', MetricCategory.DISTRIBUTION, classic_stats.ratio_percentiles_5_10, 'Ratio between contributions of the 5th user and the 10th top user'))
    metrics.append(Metric('ratio_percentiles_10_20', 'Participants prctl. 10 / 20', MetricCategory.DISTRIBUTION, classic_stats.ratio_percentiles_10_20, 'Ratio between contributions of the 10th user and the 20th top user'))

    return metrics


def generate_monowiki_metrics():
    metrics = []

    # Activity streak
    metrics.append(Metric('Current_streak', 'Active users by activity-streak', MetricCategory.ACTIVE_EDITORS_ANALYSIS, monowiki_stats.current_streak, 'BAR GRAPH: Users by the number of consecutive months they have made at least one edit in the wiki.'))
    metrics.append(Metric('Current_streak_only_mains', 'Active users by edit-streak', MetricCategory.ACTIVE_EDITORS_ANALYSIS, monowiki_stats.current_streak_only_mains, 'BAR GRAPH: Users by the number of consecutive months they have made at least one edit in the main namespace of the wiki.'))
    metrics.append(Metric('edition_on_type_pages', 'Edits in popular namespaces', MetricCategory.EDITS_ANALYSIS, monowiki_stats.edition_on_type_pages, 'BAR GRAPH: number of edits in the most popular namespaces of a wiki.'))
    metrics.append(Metric('edition_on_type_pages_extends_rest', 'Edits in other namespaces', MetricCategory.EDITS_ANALYSIS, monowiki_stats.edition_on_type_pages_extends_rest, 'BAR GRAPH: number of edits in less popular namespaces of the wiki.'))


    metrics.append(Metric('users_first_edit', 'Users by tenure', MetricCategory.ACTIVE_EDITORS_ANALYSIS, monowiki_stats.users_first_edit, 'BAR GRAPH: Users by the number of months since their first edit in the wiki.'))

    metrics.append(Metric('users_last_edit', 'Returning active editors', MetricCategory.ACTIVE_EDITORS_ANALYSIS, monowiki_stats.users_last_edit, 'BAR GRAPH: Users by the number of months since their last edit in the wiki.'))

    metrics.append(Metric('users_edits_number_of_edits', 'Active editors by experience', MetricCategory.ACTIVE_EDITORS_ANALYSIS, monowiki_stats.users_number_of_edits, 'BAR GRAPH: Users by the number of edits they have made until the previous month.'))
    metrics.append(Metric('users_edits_number_of_edits_abs', 'Active editors by experience (relative)', MetricCategory.ACTIVE_EDITORS_ANALYSIS, monowiki_stats.users_number_of_edits_abs, 'BAR GRAPH: Users by the number of edits they have made until the previous month (relative).'))

    metrics.append(Metric('type_page_users_edit', 'Active editors in namespaces', MetricCategory.ACTIVE_EDITORS_ANALYSIS, monowiki_stats.type_page_users_edit, 'BAR GRAPH: Users by the namespaces they have edited in a month.'))

    metrics.append(Metric('surviving new editor', 'Surviving new editor', MetricCategory.ACTIVE_EDITORS_ANALYSIS, monowiki_stats.surviving_new_editor, 'SCATTER GRAPH: Editor which, in the second month after being registrated, edits the wiki'))
    metrics.append(Metric('returning new editor', 'Returning new editor', MetricCategory.ACTIVE_EDITORS_ANALYSIS, monowiki_stats.returning_new_editor, 'SCATTER GRAPH: New editor who completes at least two edit sessions within 7 days afte registering.'))

    # metric to measure level of participation among different user categories
    metrics.append(Metric('number_of_edits_category', 'Edits by editor experience', MetricCategory.EDITS_ANALYSIS, monowiki_stats.number_of_edits_by_category, 'BAR GRAPH: number of editions per categories of active editors by experience.'))
    metrics.append(Metric('percentage_of_edits_category', 'Edits by editor experience (relative)', MetricCategory.EDITS_ANALYSIS, monowiki_stats.percentage_of_edits_by_category, 'BAR GRAPH: number of editions per categories of active editors by experience (relative).'))

    # area chart metrics
    metrics.append(Metric('contributorPctg_per_contributionPctg', 'editor% per contribution%', MetricCategory.ACTIVE_EDITORS_ANALYSIS, monowiki_stats.contributor_pctg_per_contributions_pctg, 'FILLED-AREA CHART: % editors per %editions (% editions fixed to 50%, 80%, 90% and 99%)'))
    metrics.append(Metric('contributorPctg_per_contributionPctg_month', 'monthly editor% per contribution%', MetricCategory.ACTIVE_EDITORS_ANALYSIS, monowiki_stats.contributor_pctg_per_contributions_pctg_per_month, 'FILLED-AREA CHART: monthly % editors per %editions (%editions fixed to 50%, 80%, 90% and 99%)'))

    # heatmap metrics
    metrics.append(Metric('edit_distributions_across_editors', 'Edit distribution across editors', MetricCategory.ACTIVE_EDITORS_ANALYSIS, monowiki_stats.edit_distributions_across_editors, 'HEATMAP: contributors (z axis) per contributions (y axis).'))
    metrics.append(Metric('bytes_difference_across_articles', 'Bytes difference across articles', MetricCategory.EDITS_ANALYSIS, monowiki_stats.bytes_difference_across_articles, 'HEATMAP: number of articles (z axis) than contain these bytes (y axis).'))
    metrics.append(Metric('changes_in_absolute_size_of_classes', 'changes in categories of active editors by experience', MetricCategory.ACTIVE_EDITORS_ANALYSIS, monowiki_stats.changes_in_absolute_size_of_editor_classes, 'HEATMAP: increment or decrement (z axis) of an active editor category (y axis).'))
    metrics.append(Metric('distribution_editors_between_articles_edited_each_month', 'Monthly distribution of editors across articles', MetricCategory.ACTIVE_EDITORS_ANALYSIS, monowiki_stats.distribution_editors_between_articles_edited_each_month, 'HEATMAP:.'))
    metrics.append(Metric('edition_on_pages', 'Edits on pages', MetricCategory.EDITS_ANALYSIS, monowiki_stats.edition_on_pages, 'HEATMAP:'))
    metrics.append(Metric('revision_on_pages', 'Revisions on pages', MetricCategory.EDITS_ANALYSIS, monowiki_stats.revision_on_pages, 'HEATMAP:'))

    return metrics


def generate_metrics():
    metrics = generate_classic_metrics() + generate_monowiki_metrics()

    # keep order of insertion when plotting graphs inserting 'index_' at the beginning
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

