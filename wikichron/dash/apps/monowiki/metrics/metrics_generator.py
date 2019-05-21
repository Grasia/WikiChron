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
    

    # Users

   
    # metric 2
    #metrics.append(Metric('Activity_streak_1', 'Activity streak 1', MetricCategory.USERS, stats.current_streak_this_month, 'Users editing the wiki for 1 month in a row.'))
    #metrics.append(Metric('Activity_streak_2_3', 'Activity streak 2', MetricCategory.USERS, stats.current_streak_2_or_3_months_in_a_row, 'Users editing the wiki for 2 or 3 months in a row'))
    #metrics.append(Metric('Activity_streak_4_6', 'Activity streak 3', MetricCategory.USERS, stats.current_streak_4_or_6_months_in_a_row, 'Users editing the wiki for 4 or 6 months in a row'))
    #metrics.append(Metric('Activity_streak_6', 'Activity streak 4', MetricCategory.USERS, stats.current_streak_more_than_six_months_in_a_row, 'Users editing the wiki for more than 6 months in a row'))
    metrics.append(Metric('Current_streak', 'Active users by activity-streak', MetricCategory.ACTIVE_EDITORS_ANALYSIS, stats.current_streak, 'BAR GRAPH: Users by the number of consecutive months they have made at least one edit in the wiki.'))
    metrics.append(Metric('Current_streak_only_mains', 'Active users by edit-streak', MetricCategory.ACTIVE_EDITORS_ANALYSIS, stats.current_streak_only_mains, 'BAR GRAPH: Users by the number of consecutive months they have made at least one edit in the main of the wiki.'))
    metrics.append(Metric('edition_on_type_pages', 'Edition on different type pages', MetricCategory.ACTIVE_EDITORS_ANALYSIS, stats.edition_on_type_pages, 'BAR GRAPH:'))
    metrics.append(Metric('edition_on_type_pages_extends_rest', 'Edition on different type pages rest', MetricCategory.ACTIVE_EDITORS_ANALYSIS, stats.edition_on_type_pages_extends_rest, 'BAR GRAPH:'))
    
    # metric 3
    #metrics.append(Metric('users_first_edit_between_1_3_months_ago', 'Users first edit 1', MetricCategory.USERS, stats.users_first_edit_between_1_3_months_ago, 'Users whose first edition was between 1 and 3 months ago'))
    #metrics.append(Metric('users_first_edit_between_4_6_months_ago', 'Users first edit 2', MetricCategory.USERS, stats.users_first_edit_between_4_6_months_ago, 'Users whose first edition was between 4 and 6 months ago'))
    #metrics.append(Metric('users_first_edit_more_than_6_months_ago', 'Users first edit 3', MetricCategory.USERS, stats.users_first_edit_more_than_6_months_ago, 'Users whose first edition was more than 6 months ago'))
    metrics.append(Metric('users_first_edit', 'Users by antiquity', MetricCategory.ACTIVE_EDITORS_ANALYSIS, stats.users_first_edit, 'BAR GRAPH: Users by the number of months since their first edit in the wiki.'))

    # metric 4
    #metrics.append(Metric('users_last_edit_1_month_ago', 'users last edit 1', MetricCategory.USERS, stats.users_last_edit_1_month_ago, 'Users editing in month X whose last edit was in month X-1'))
    #metrics.append(Metric('users_last_edit_2_or_3_months_ago', 'users last edit 2', MetricCategory.USERS, stats.users_last_edit_2_or_3_months_ago, 'Users editing in month X whose last edit was in month X-2 or X-3'))
    #metrics.append(Metric('users_last_edit_4_or_5_or_6_months_ago', 'Users last edit 3', MetricCategory.USERS, stats.users_last_edit_4_or_5_or_6_months_ago, 'Users editing in month X whose last edit was in month X-4, X-5 or X-6'))
    #metrics.append(Metric('users_last_edit_more_than_6_months_ago', 'users last edit 4', MetricCategory.USERS, stats.users_last_edit_more_than_6_months_ago, 'Users editing in month X whose last edit was in any month > X-6'))
    metrics.append(Metric('users_last_edit', 'Returning active editors', MetricCategory.ACTIVE_EDITORS_ANALYSIS, stats.users_last_edit, 'BAR GRAPH: Users by the number of months since their last edit in the wiki.'))

    # metric 5
    #metrics.append(Metric('users_edits_between_1_4', 'users #edits 1', MetricCategory.USERS, stats.users_number_of_edits_between_1_and_4, 'Users that have completed between 1 and 4 editions until month X-1 (included)'))
    #metrics.append(Metric('users_edits_between_5_24', 'users #edits 2', MetricCategory.USERS, stats.users_number_of_edits_between_5_and_24, 'Users that have completed between 5 and 24 editions until month X-1 (included)'))
    #metrics.append(Metric('users_edits_between_25_99', 'users #edits 3', MetricCategory.USERS, stats.users_number_of_edits_between_25_and_99, 'Users that have completed between 25 and 99 editions until month X-1 (included)'))
    #metrics.append(Metric('users_edits_highEq_100', 'users #edits 4', MetricCategory.USERS, stats.users_number_of_edits_highEq_100, 'Users that have completed >= 100 editions until month X-1 (included)'))
    metrics.append(Metric('users_edits_number_of_edits', 'Active editors by experience', MetricCategory.ACTIVE_EDITORS_ANALYSIS, stats.users_number_of_edits, 'BAR GRAPH: Users by the number of edits they have made until the previous month.'))
    metrics.append(Metric('users_edits_number_of_edits_abs', 'Active editors by experience (relative)', MetricCategory.ACTIVE_EDITORS_ANALYSIS, stats.users_number_of_edits_abs, 'BAR GRAPH: Users by the number of edits they have made until the previous month (relative).'))

# metric 6: wikimedia
# metric 7
# metric 8

    # metrics 10 and 9: users editing main, template and talk pages
    #metrics.append(Metric('users_main_page', 'Users main page', MetricCategory.USERS, stats.users_main_page, 'Users who have edited a main page'))
    #metrics.append(Metric('users_template_page', 'Users template page', MetricCategory.USERS, stats.users_template_page, 'Users who have edited a template page'))
    #metrics.append(Metric('talk_page_users', 'Users talk page', MetricCategory.USERS, stats.talk_page_users, 'Users that have edited a talk page.'))
    metrics.append(Metric('type_page_users_edit', 'Active editors in namespaces', MetricCategory.ACTIVE_EDITORS_ANALYSIS, stats.type_page_users_edit, 'BAR GRAPH: Users by the namespaces they have edited in a month.'))
    
    metrics.append(Metric('surviving new editor', 'Surviving new editor', MetricCategory.ACTIVE_EDITORS_ANALYSIS, stats.surviving_new_editor, 'SCATTER GRAPH: Editor which, in the second month after being registrated, edits the wiki'))
    metrics.append(Metric('returning new editor', 'Returning new editor', MetricCategory.ACTIVE_EDITORS_ANALYSIS, stats.returning_new_editor, 'SCATTER GRAPH: New editor who completes at least two edit sessions within 7 days afte registering.'))
#metric to measure level of participation among different user categories
    metrics.append(Metric('number_of_edits_category', 'Edits by editor experience', MetricCategory.EDITS_ANALYSIS, stats.number_of_edits_by_category, 'BAR GRAPH: number of editions per categories of active editors by experience.'))
    metrics.append(Metric('percentage_of_edits_category', 'Edits by editor experience (relative)', MetricCategory.EDITS_ANALYSIS, stats.percentage_of_edits_by_category, 'BAR GRAPH: number of editions per categories of active editors by experience (relative).'))
    
# area chart metrics
    metrics.append(Metric('contributorPctg_per_contributionPctg', 'editor% per contribution%', MetricCategory.ACTIVE_EDITORS_ANALYSIS, stats.contributor_pctg_per_contributions_pctg, 'FILLED-AREA CHART: % editors per %editions (% editions fixed to 50%, 80%, 90% and 99%)'))
    metrics.append(Metric('contributorPctg_per_contributionPctg_month', 'monthly editor% per contribution%', MetricCategory.ACTIVE_EDITORS_ANALYSIS, stats.contributor_pctg_per_contributions_pctg_per_month, 'FILLED-AREA CHART: monthly % editors per %editions (%editions fixed to 50%, 80%, 90% and 99%)'))

# heatmap metrics
    metrics.append(Metric('edit_distributions_across_editors', 'Edit distribution across editors', MetricCategory.ACTIVE_EDITORS_ANALYSIS, stats.edit_distributions_across_editors, 'HEATMAP: contributors (z axis) per contributions (y axis).'))
    metrics.append(Metric('bytes_difference_across_articles', 'Bytes difference across articles', MetricCategory.EDITS_ANALYSIS, stats.bytes_difference_across_articles, 'HEATMAP: number of articles (z axis) than contain these bytes (y axis).'))
    metrics.append(Metric('changes_in_absolute_size_of_classes', 'changes in categories of active editors by experience', MetricCategory.ACTIVE_EDITORS_ANALYSIS, stats.changes_in_absolute_size_of_editor_classes, 'HEATMAP: increment or decrement (z axis) of an active editor category (y axis).'))
    metrics.append(Metric('distribution_editors_between_articles_edited_each_month', 'Monthly distribution of editors across articles', MetricCategory.ACTIVE_EDITORS_ANALYSIS, stats.distribution_editors_between_articles_edited_each_month, 'HEATMAP:.'))
    metrics.append(Metric('edition_on_pages', 'Edits on pages', MetricCategory.EDITS_ANALYSIS, stats.edition_on_pages, 'HEATMAP:'))
    metrics.append(Metric('revision_on_pages', 'Revisions on pages', MetricCategory.EDITS_ANALYSIS, stats.revision_on_pages, 'HEATMAP:'))

    
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

'''def main():
    print (generate_metrics())
    return

if __name__ == '__main__':
    main()'''

