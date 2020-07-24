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
from .metricClasses.HeatMap import HeatMap
from .metricClasses.BarGraph import BarGraph
from .metricClasses.AreaChart import AreaChart
from .metricClasses.LineGraph import LineGraph

def generate_classic_metrics():
    metrics = []

    # Pages
    metrics.append(LineGraph('pages_new', 'New pages', MetricCategory.PAGES, classic_stats.pages_new, 'Number of new pages created per month', 'New pages'))
    metrics.append(LineGraph('pages_main_new', 'New articles', MetricCategory.PAGES, classic_stats.pages_main_new, 'Number of new articles (main content) created per month', 'New articles'))
    metrics.append(LineGraph('pages_edited', 'Pages edited', MetricCategory.PAGES, classic_stats.pages_edited, 'Number of different pages edited per month', 'Pages edited'))
    metrics.append(LineGraph('main_edited', 'Articles edited', MetricCategory.PAGES, classic_stats.main_edited, 'Number of different articles edited per month', 'Articles edited'))
    metrics.append(LineGraph('pages_accum', 'Total pages', MetricCategory.PAGES, classic_stats.pages_accum, 'Total of pages accumulated at every month', 'Total pages'))
    metrics.append(LineGraph('pages_main_accum', 'Total articles', MetricCategory.PAGES, classic_stats.pages_main_accum, 'Total of articles (main content) at every month', 'Total articles'))

    # Editions
    metrics.append(LineGraph('edits', 'Edits in pages', MetricCategory.EDITIONS, classic_stats.edits, 'Editions to any part of the wiki grouped by month', 'Edits in pages'))
    metrics.append(LineGraph('edits_main_content', 'Edits in articles', MetricCategory.EDITIONS, classic_stats.edits_main_content, 'Editions to articles (main content) per month', 'Edits in articles'))
    metrics.append(LineGraph('edits_article_talk', 'Edits in articles talk', MetricCategory.EDITIONS, classic_stats.edits_article_talk, 'Editions to article discussion pages', 'Edits in articles talk'))
    metrics.append(LineGraph('edits_user_talk', 'Edits in user talk', MetricCategory.EDITIONS, classic_stats.edits_user_talk, 'Editions to user discussion pages', 'Edits in user talk'))
    metrics.append(LineGraph('edits_accum', 'Total edits in pages', MetricCategory.EDITIONS, classic_stats.edits_accum, 'Total editions to any part of the wiki accumulated at every month', 'Total edits in pages'))
    metrics.append(LineGraph('edits_main_content_accum', 'Total edits in articles', MetricCategory.EDITIONS, classic_stats.edits_main_content_accum, 'Editions to articles accumulated at every month', 'Total edits in articles'))

    # Users
    metrics.append(LineGraph('users_new', 'New users', MetricCategory.USERS, classic_stats.users_new, 'Users who have made at least one edition grouped by the month they did their first edit.', 'New users'))
    metrics.append(LineGraph('users_new_registered', 'New registered users', MetricCategory.USERS, classic_stats.users_new_registered, 'New users registration per month who have made at least one edition.', 'New registered users'))
    metrics.append(LineGraph('users_new_anonymous', 'New anonymous users', MetricCategory.USERS, classic_stats.users_new_anonymous, 'Anonymous users who made at least one edition grouped by the month they did their first edit. Anonymous are identified by their ip.', 'New anonymous users'))
    metrics.append(LineGraph('users_accum', 'Total users', MetricCategory.USERS, classic_stats.users_accum, 'Users who have made at least one edition accumulated at every month.', 'Total users'))
    metrics.append(LineGraph('users_registered_accum', 'Total registered users', MetricCategory.USERS, classic_stats.users_registered_accum, 'Total registered users at every month. Note that users have to have made at least one edition and they have to be logged with their account when they did that edition.', 'Total registered users'))
    metrics.append(LineGraph('users_anonymous_accum', 'Total anonymous users', MetricCategory.USERS, classic_stats.users_anonymous_accum, 'Anonymous users who have made at least one edition accumulated at every month. Anonymous are identified by their ip.', 'Total anonymous users'))
    metrics.append(LineGraph('users_active', 'Active users', MetricCategory.USERS, classic_stats.users_active, 'Number of users who have made at least one contribution in a month.', 'Active users'))
    metrics.append(LineGraph('users_active_registered', 'Active registered users', MetricCategory.USERS, classic_stats.users_registered_active, 'Number of registered users who have made at least one contribution in a month.', 'Active registered users'))
    metrics.append(LineGraph('users_active_anonymous', 'Active anonymous users', MetricCategory.USERS, classic_stats.users_anonymous_active, 'Number of anonymous users who have made at least one contribution in a month.', 'Active anonymous users'))
    metrics.append(LineGraph('users_active_more_than_4', 'Active users with > 4 edits', MetricCategory.USERS, classic_stats.users_active_more_than_4_editions, 'Active users who have made more than 4 editions in a month.', 'Active users with > 4 edits'))
    metrics.append(LineGraph('users_active_more_than_24', 'Active users with > 24 edits', MetricCategory.USERS, classic_stats.users_active_more_than_24_editions, 'Active users who have made more than 24 editions in a month.', 'Active users with > 24 edits'))
    metrics.append(LineGraph('users_active_more_than_99', 'Active users with > 99 edits', MetricCategory.USERS, classic_stats.users_active_more_than_99_editions, 'Active users who have made more than 99 editions in a month.', 'Active users with > 99 edits'))
    metrics.append(LineGraph('returning_new_editors', 'Returning new editors', MetricCategory.USERS, classic_stats.returning_new_editors, "Number of new users who completes at least two edit sessions (60') within the first 30 days since registration. Based on a WMF's metric.", 'Returning new editors'))
    metrics.append(LineGraph('surviving_new_editors', 'Surviving new editors', MetricCategory.USERS, classic_stats.surviving_new_editors, "Numer of new users who completes at least one edit within the first 30 days since registration and also completes another edit in the survival period, (i.e. the following 30 days). Based on a WMF's metric.", 'Surviving new editors',))

    # RATIO
    metrics.append(LineGraph('edits_per_users_monthly', 'Edits per users', MetricCategory.RATIOS, classic_stats.edits_per_users_monthly, 'Number of edits for every month per number of active users that month', 'Edits per users'))
    metrics.append(LineGraph('edits_in_articles_per_users_monthly', 'Article edits per user', MetricCategory.RATIOS, classic_stats.edits_in_articles_per_users_monthly, 'Number of edits in articles per number of users for each month', 'Article edits per user'))
    metrics.append(LineGraph('edits_per_page_monthly', 'Edits per edited pages', MetricCategory.RATIOS, classic_stats.edits_per_pages_monthly, 'Number of edits for every month per number of pages edited that month', 'Edits per edited pages'))
    metrics.append(LineGraph('percentage_edits_by_anonymous_monthly', 'Anonymous edits (%)', MetricCategory.RATIOS, classic_stats.percentage_edits_by_anonymous_monthly, 'Percentage of edits made by anonymous users of the total edits.', 'Anonymous edits (%)'))
    metrics.append(LineGraph('edits_in_articles_per_users_accum', 'Total articles edits per user', MetricCategory.RATIOS, classic_stats.edits_in_articles_per_users_accum, 'Number of total edits in articles per number of users until a given month', 'Total articles edits per user'))
    metrics.append(LineGraph('edits_per_pages_accum', 'Total edits per page', MetricCategory.RATIOS, classic_stats.edits_per_pages_accum, 'Number of total edits per number of total pages' 'Total edits per page', 'Total edits per page'))
    metrics.append(LineGraph('percentage_edits_by_anonymous_accum', 'Total anonymous edits (%)', MetricCategory.RATIOS, classic_stats.percentage_edits_by_anonymous_accum, 'Percentage, per month, of edits made by anonymous users of the total edits.', 'Total anonymous edits (%)'))

    # RETENTION
    
    # DISTRIBUTION
    metrics.append(LineGraph('gini_accum', 'Gini coefficient', MetricCategory.DISTRIBUTION, classic_stats.gini_accum, 'Gini coefficient (accumulated)', 'Gini coefficient'))
    metrics.append(LineGraph('ratio_10_90', '10:90 ratio', MetricCategory.DISTRIBUTION, classic_stats.ratio_10_90, 'Contributions of the top ten percent more active users between the 90% percent less active', '10:90 ratio'))
    metrics.append(LineGraph('ratio_percentiles_max_5', 'Participants prctl. top / 5', MetricCategory.DISTRIBUTION, classic_stats.ratio_percentiles_max_5, 'Ratio between contributions of the top and the 5th top users', 'Participants prctl. top / 5'))
    metrics.append(LineGraph('ratio_percentiles_max_10', 'Participants prctl. top / 10', MetricCategory.DISTRIBUTION, classic_stats.ratio_percentiles_max_10, 'Ratio between contributions of the top user and the 10th top user', 'Participants prctl. top / 10'))
    metrics.append(LineGraph('ratio_percentiles_max_20', 'Participants prctl. top / 20', MetricCategory.DISTRIBUTION, classic_stats.ratio_percentiles_max_20, 'Ratio between contributions of the top user and the 20th top user', 'Participants prctl. top / 20'))
    metrics.append(LineGraph('ratio_percentiles_5_10', 'Participants prctl. 5 / 10', MetricCategory.DISTRIBUTION, classic_stats.ratio_percentiles_5_10, 'Ratio between contributions of the 5th user and the 10th top user', 'Participants prctl. 5 / 10'))
    metrics.append(LineGraph('ratio_percentiles_10_20', 'Participants prctl. 10 / 20', MetricCategory.DISTRIBUTION, classic_stats.ratio_percentiles_10_20, 'Ratio between contributions of the 10th user and the 20th top user', 'Participants prctl. 10 / 20'))

    return metrics


def generate_monowiki_metrics():
    metrics = []

	# DISTRIBUTION_OF_ACTIVE_REGISTERED_USERS
    metrics.append(BarGraph('users_edits_number_of_edits', 'By editing experience', MetricCategory.DISTRIBUTION_OF_ACTIVE_REGISTERED_USERS, monowiki_stats.users_number_of_edits, 'Distribution of editors by their number of previous edits', 'Dist. of active registered users by editing experience'))
    metrics.append(BarGraph('users_edits_number_of_edits_abs', 'By editing experience (in %)', MetricCategory.DISTRIBUTION_OF_ACTIVE_REGISTERED_USERS, monowiki_stats.users_number_of_edits_abs, 'Distribution of editors by their number of previous edits (in %)', 'Dist. of active registered users by editing experience (in %)'))
    metrics.append(BarGraph('users_first_edit', 'By tenure', MetricCategory.DISTRIBUTION_OF_ACTIVE_REGISTERED_USERS, monowiki_stats.users_first_edit, 'Distribution of editors by their time participating in the wiki', 'Dist. of active registered users by tenure'))
    metrics.append(BarGraph('users_edits_tenure_abs', 'By tenure (in %)', MetricCategory.DISTRIBUTION_OF_ACTIVE_REGISTERED_USERS, monowiki_stats.users_first_edit_abs, 'Distribution of editors by their time participating in the wiki (in %)', 'Dist. of active registered users by tenure (in %)'))
    metrics.append(BarGraph('Current_streak', 'By edit streak', MetricCategory.DISTRIBUTION_OF_ACTIVE_REGISTERED_USERS, monowiki_stats.current_streak, 'Distribution of editors by their last streak editing the wiki', 'Dist. of active registered users by edit streak'))
    metrics.append(BarGraph('Current_streak_only_mains', 'By edit in article streak', MetricCategory.DISTRIBUTION_OF_ACTIVE_REGISTERED_USERS, monowiki_stats.current_streak_only_mains, 'Distribution of editors by their last streak editing the wiki (only articles)', 'Dist. of active registered users by edit in article streak'))
    metrics.append(BarGraph('users_last_edit', 'By date of the last edit', MetricCategory.DISTRIBUTION_OF_ACTIVE_REGISTERED_USERS, monowiki_stats.users_last_edit, 'Distribution of editors by their last edit in the wiki', 'Dist. of active registered users by date of the last edit'))
    metrics.append(BarGraph('users_last_edit_abs', 'By date of the last edit (in %)', MetricCategory.DISTRIBUTION_OF_ACTIVE_REGISTERED_USERS, monowiki_stats.users_last_edit_abs, 'Distribution of editors by their last edit in the wiki (in %)', 'Dist. of active registered users by date of the last edit (in %)'))
    metrics.append(BarGraph('type_page_users_edit', 'By namespace edited', MetricCategory.DISTRIBUTION_OF_ACTIVE_REGISTERED_USERS, monowiki_stats.users_in_namespaces, 'Distribution of editors by the namespace edited', 'Dist. of active registered users by namespace edited'))
    # Doesn't work properly, it is not mandatory
    #metrics.append(BarGraph('type_page_users_edit_extends', 'By other namespace edited', MetricCategory.DISTRIBUTION_OF_ACTIVE_REGISTERED_USERS, monowiki_stats.users_in_namespaces_extends, 'Distribution of editors by other namespace edited', 'Dist. of active registered users by other namespace edited'))

    # DISTRIBUTION_OF_EDITS_ACROSS_REGISTERED_USERS
    metrics.append(BarGraph('number_of_edits_experience_abs', 'By editing experience', MetricCategory.DISTRIBUTION_OF_EDITS_ACROSS_REGISTERED_USERS, monowiki_stats.number_of_edits_by_experience_abs, 'Distribution of edits across distribution of editors by their number of previous edits', 'Dist. of edits across registered users by editing experience'))
    metrics.append(BarGraph('number_of_edits_experience_rel', 'By editing experience (in %)', MetricCategory.DISTRIBUTION_OF_EDITS_ACROSS_REGISTERED_USERS, monowiki_stats.number_of_edits_by_experience_rel, 'Distribution of edits across distribution of editors by their number of previous edits in percentage', 'Dist. of edits across registered users by editing experience (in %)'))
    metrics.append(BarGraph('number_of_edits_tenure', 'By tenure', MetricCategory.DISTRIBUTION_OF_EDITS_ACROSS_REGISTERED_USERS, monowiki_stats.number_of_edits_by_tenure, 'Distribution of edits across distribution of editors by their time participating in the wiki', 'Dist. of edits across registered users by tenure'))
    metrics.append(BarGraph('percentage_of_edits_tenure', 'By tenure (in %)', MetricCategory.DISTRIBUTION_OF_EDITS_ACROSS_REGISTERED_USERS, monowiki_stats.number_of_edits_by_tenure_abs, 'Distribution of edits across distribution of editors by their time participating in the wiki (in %)', 'Dist. of edits across registered users by tenure (in %)'))
    metrics.append(BarGraph('edits_by_current_streak', 'By edit streak', MetricCategory.DISTRIBUTION_OF_EDITS_ACROSS_REGISTERED_USERS, monowiki_stats.edits_by_current_streak, 'Distribution of edits across distribution of editors by their last streak editing the wiki', 'Dist. of edits across registered users by edit streak'))
    metrics.append(BarGraph('number_of_edits_last_edit', 'By date of the last edit', MetricCategory.DISTRIBUTION_OF_EDITS_ACROSS_REGISTERED_USERS, monowiki_stats.number_of_edits_by_last_edit, 'Distribution of edits across distribution of editors by their last edit in the wiki', 'Dist. of edits across registered users by date of the last edit'))
    metrics.append(BarGraph('edition_on_type_pages', 'By namespace edited', MetricCategory.DISTRIBUTION_OF_EDITS_ACROSS_REGISTERED_USERS, monowiki_stats.edition_on_type_pages, 'Distribution of edits in the most popular namespaces', 'Dist. of edits across registered users by namespace edited'))

    # DISTRIBUTION_OF_EDITS
    metrics.append(AreaChart('contributorPctg_per_contributionPctg', 'Percentage of registered users vs percentage of edits made (total)', MetricCategory.DISTRIBUTION_OF_EDITS, monowiki_stats.contributor_pctg_per_contributions_pctg, 'Percentage of editors across percentege of editions (Percentage of editions fixed to 50%, 80%, 90% and 99%)', 'Percentage of registered users making a percentage of edits'))
    metrics.append(AreaChart('contributorPctg_per_contributionPctg_month', 'Percentage of registered users vs percentage of edits made (monthly)', MetricCategory.DISTRIBUTION_OF_EDITS, monowiki_stats.contributor_pctg_per_contributions_pctg_per_month, 'Monthly percentage of editors aross percentage of editions (Percentage of editions fixed to 50%, 80%, 90% and 99%)', 'Percentage of registered users making a percentage of edits (monthly)'))
    return metrics


def generate_metrics():
    metrics = generate_classic_metrics() + generate_monowiki_metrics()

    # keep order of insertion when plotting graphs inserting 'index_' at the beginning
    #  for every metric code.
    # NOTE: Possibly, It'll be changed in the future by an specifc attr: "order"
    #  in the GUI side, in order to be able to reorder the plots.
    for idx, metric in enumerate(metrics):
        metrics[idx].code = f"{idx}_{metric.code}"

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
