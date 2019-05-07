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
    metrics.append(Metric('Current_streak', 'Active users by edit-streak', MetricCategory.BAR, stats.current_streak, 'Users whose current streak of editions is: 1) 1 month. 2) Btw. 2 and 3 months in a row. 3) Btw. 4 and 6 months in a row. 4) More than 6 months in a row.'))

    # metric 3
    #metrics.append(Metric('users_first_edit_between_1_3_months_ago', 'Users first edit 1', MetricCategory.USERS, stats.users_first_edit_between_1_3_months_ago, 'Users whose first edition was between 1 and 3 months ago'))
    #metrics.append(Metric('users_first_edit_between_4_6_months_ago', 'Users first edit 2', MetricCategory.USERS, stats.users_first_edit_between_4_6_months_ago, 'Users whose first edition was between 4 and 6 months ago'))
    #metrics.append(Metric('users_first_edit_more_than_6_months_ago', 'Users first edit 3', MetricCategory.USERS, stats.users_first_edit_more_than_6_months_ago, 'Users whose first edition was more than 6 months ago'))
    metrics.append(Metric('users_first_edit', 'Users first edit', MetricCategory.BAR, stats.users_first_edit, 'Users whose first edition was: 0) This month. 1) Between 1 and 3 months ago. 2) Between 4 and 6 months ago. 3) More than 6 months ago.'))

    # metric 4
    #metrics.append(Metric('users_last_edit_1_month_ago', 'users last edit 1', MetricCategory.USERS, stats.users_last_edit_1_month_ago, 'Users editing in month X whose last edit was in month X-1'))
    #metrics.append(Metric('users_last_edit_2_or_3_months_ago', 'users last edit 2', MetricCategory.USERS, stats.users_last_edit_2_or_3_months_ago, 'Users editing in month X whose last edit was in month X-2 or X-3'))
    #metrics.append(Metric('users_last_edit_4_or_5_or_6_months_ago', 'Users last edit 3', MetricCategory.USERS, stats.users_last_edit_4_or_5_or_6_months_ago, 'Users editing in month X whose last edit was in month X-4, X-5 or X-6'))
    #metrics.append(Metric('users_last_edit_more_than_6_months_ago', 'users last edit 4', MetricCategory.USERS, stats.users_last_edit_more_than_6_months_ago, 'Users editing in month X whose last edit was in any month > X-6'))
    metrics.append(Metric('users_last_edit', 'Returning active editors', MetricCategory.BAR, stats.users_last_edit, 'Users whose last edition was: 0) This month. 1) 1 month ago. 2) Between 2 and 3 months ago. 3) Between 4 and 6 months ago. 4) More than 6 months ago.'))

    # metric 5
    #metrics.append(Metric('users_edits_between_1_4', 'users #edits 1', MetricCategory.USERS, stats.users_number_of_edits_between_1_and_4, 'Users that have completed between 1 and 4 editions until month X-1 (included)'))
    #metrics.append(Metric('users_edits_between_5_24', 'users #edits 2', MetricCategory.USERS, stats.users_number_of_edits_between_5_and_24, 'Users that have completed between 5 and 24 editions until month X-1 (included)'))
    #metrics.append(Metric('users_edits_between_25_99', 'users #edits 3', MetricCategory.USERS, stats.users_number_of_edits_between_25_and_99, 'Users that have completed between 25 and 99 editions until month X-1 (included)'))
    #metrics.append(Metric('users_edits_highEq_100', 'users #edits 4', MetricCategory.USERS, stats.users_number_of_edits_highEq_100, 'Users that have completed >= 100 editions until month X-1 (included)'))
    metrics.append(Metric('users_edits_number_of_edits', 'Active editors by experience', MetricCategory.BAR, stats.users_number_of_edits, 'Users whose number of editions in a month is: 1) Between 1 and 4 editions. 2) Between 5 and 24 editions. 3) Between 25 and 99 editions. 4) Higher than 99.'))
    metrics.append(Metric('users_edits_number_of_edits_abs', 'Active editors by experience (relative)', MetricCategory.BAR, stats.users_number_of_edits_abs, ''))

# metric 6: wikimedia
# metric 7
# metric 8

    # metrics 10 and 9: users editing main, template and talk pages
    #metrics.append(Metric('users_main_page', 'Users main page', MetricCategory.USERS, stats.users_main_page, 'Users who have edited a main page'))
    #metrics.append(Metric('users_template_page', 'Users template page', MetricCategory.USERS, stats.users_template_page, 'Users who have edited a template page'))
    #metrics.append(Metric('talk_page_users', 'Users talk page', MetricCategory.USERS, stats.talk_page_users, 'Users that have edited a talk page.'))
    metrics.append(Metric('type_page_users_edit', 'Active editors in namespaces', MetricCategory.BAR, stats.type_page_users_edit, 'Users who have edited: 1) A main page. 2) A template page. 3) Article talk.'))

#metric to measure level of participation among different user categories
    metrics.append(Metric('number_of_edits_category', 'Edits by editor experience', MetricCategory.BAR, stats.number_of_edits_by_category, 'number of editions done by each one of the following user categories: 1) users that have done between 1 and 4 editions in all the history of the wiki. 2) users that have done between 5 and 24 editions in all the history of the wiki. 3) users that have done between 25 and 99 editions in all the history of the wiki. 4) users that have done a number greater or equal to 100 editions in all the history of the wiki. 5) New users each month.'))

    metrics.append(Metric('percentage_of_edits_category', 'Edits by editor experience (relative)', MetricCategory.BAR, stats.percentage_of_edits_by_category, '% of editions done by each one of the following user categories: 1) users that have done between 1 and 4 editions in all the history of the wiki. 2) users that have done between 5 and 24 editions in all the history of the wiki. 3) users that have done between 25 and 99 editions in all the history of the wiki. 4) users that have done a number greater or equal to 100 editions in all the history of the wiki. 5) New users each month.'))
    
# area chart metrics
    metrics.append(Metric('contributorPctg_per_contributionPctg', 'editor% per contribution%', MetricCategory.AREACHART, stats.contributor_pctg_per_contributions_pctg, 'editor % contributing to do a %Y of the total editions of the wiki until that month, with Y ∈ {50, 80, 90, 99}'))

# heatmap metrics
    metrics.append(Metric('number_of_editors_per_contributions', 'num editors per contributions', MetricCategory.HEATMAPS, stats.number_of_editors_per_contributions, 'Heatmap that shows the number of editors per contributions(y axis = number of contributions and z axis = number of editors)'))
    metrics.append(Metric('changes_in_absolute_size_of_classes', 'changes in classes of active editors by experience', MetricCategory.HEATMAPS, stats.changes_in_absolute_size_of_editor_classes, 'Heatmap that shows the changes in absolute size of active editor by experience classes: a darker color means there are less users than the previous month, and a lighter color means the number of users of a class has increased.'))
    
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

