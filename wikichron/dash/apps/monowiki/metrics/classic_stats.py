#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   stats.py

   Descp:

   Created on: 14-nov-2017

   Copyright 2017-2018 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

import pandas as pd
import numpy as np
import math
import inequality_coefficients as ineq

# CONSTANTS
MINIMAL_USERS_GINI = 20
MINIMAL_USERS_PERCENTIL_MAX_5 = 100
MINIMAL_USERS_PERCENTIL_MAX_10 = 50
MINIMAL_USERS_PERCENTIL_MAX_20 = 25
MINIMAL_USERS_PERCENTIL_5_10 = 100
MINIMAL_USERS_PERCENTIL_10_20 = 50
MINIMAL_USERS_RATIO_10_90 = 10


def calculate_index_all_months(data):
    monthly_data = data.groupby(pd.Grouper(key='timestamp', freq='MS'))
    index = monthly_data.size().index
    return index

# Pages


def pages_new(data, index):
    # We use the fact that data is sorted first by page_title and them by revision_id
    # If we drop publicates we will get the first revision for each page_title, which
    #  corresponds with the date it was created.
    pages = data.drop_duplicates('page_id')
    series = pages.groupby(pd.Grouper(key='timestamp', freq='MS')).size()
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series


def pages_accum(data, index):
    return (pages_new(data, index).cumsum())


def pages_main_new(data, index):
    pages = data.drop_duplicates('page_id')
    main_pages = pages[pages['page_ns'] == 0]
    series = main_pages.groupby(pd.Grouper(key='timestamp', freq='MS')).size()
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series


def pages_main_accum(data, index):
    return (pages_main_new(data, index).cumsum())


def pages_edited(data, index):
    monthly_data = data.groupby([pd.Grouper(key='timestamp', freq='MS')])
    series = monthly_data.apply(lambda x: len(x.page_id.unique()))
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series


def main_edited(data, index):
    main_pages = data[data['page_ns'] == 0]
    monthly_data = main_pages.groupby([pd.Grouper(key='timestamp', freq='MS')])
    series = monthly_data.apply(lambda x: len(x.page_id.unique()))
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series

########################################################################

# Editions


def edits(data, index):
    monthly_data = data.groupby(pd.Grouper(key='timestamp', freq='MS'))
    series = monthly_data.size()
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series


def edits_accum(data, index):
    return (edits(data, index).cumsum())


def edits_main_content(data, index):
    edits_main_data = data[data['page_ns'] == 0]
    return (edits(edits_main_data, index))


def edits_main_content_accum(data, index):
    return (edits_main_content(data, index).cumsum())


def edits_article_talk(data, index):
    edits_talk_data = data[data['page_ns'] == 1]
    return (edits(edits_talk_data, index))


def edits_user_talk(data, index):
    edits_talk_data = data[data['page_ns'] == 3]
    return (edits(edits_talk_data, index))

########################################################################

# Users

##### Helper functions #####


def users_active_more_than_x_editions(data, index, x):
    monthly_edits = data.groupby([pd.Grouper(key='timestamp', freq='MS'), 'contributor_id']).size()
    monthly_edits_filtered = monthly_edits[monthly_edits > x].to_frame(name='pages_edited').reset_index()
    series = monthly_edits_filtered.groupby(pd.Grouper(key='timestamp', freq='MS')).size()
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series


##### callable users metrics #####


def users_new(data, index):
    users = data.drop_duplicates('contributor_id')
    series = users.groupby(pd.Grouper(key='timestamp', freq='MS')).size()
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series


def users_accum(data, index):
    return (users_new(data, index).cumsum())


def users_new_anonymous(data, index):
    users = data.drop_duplicates('contributor_id')
    anonymous_users = users[users['contributor_name'] == 'Anonymous']
    series = anonymous_users.groupby(pd.Grouper(key='timestamp', freq='MS')).size()
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series


def users_anonymous_accum(data, index):
    return (users_new_anonymous(data, index).cumsum())


def users_new_registered(data, index):
    users = data.drop_duplicates('contributor_id')
    non_anonymous_users = users[users['contributor_name'] != 'Anonymous']
    series = non_anonymous_users.groupby(pd.Grouper(key='timestamp', freq='MS')).size()
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series


def users_registered_accum(data, index):
    return (users_new_registered(data, index).cumsum())


def users_active(data, index):
    return users_active_more_than_x_editions(data, index, 0)


# this metric is the same as the users_active, but getting rid of anonymous users
def users_registered_active(data, index):
    # get rid of anonymous users and procceed as it was done in the previous metric.
    user_registered = data[data['contributor_name'] != 'Anonymous']
    return users_active(user_registered, index)


# this metric is the complementary to users_registered_active: now, we get rid of registered users and focus on anonymous users.
def users_anonymous_active(data, index):
    user_anonymous = data[data['contributor_name'] == 'Anonymous']
    return users_active(user_anonymous, index)


# this metric gets, per month, those users who have contributed to the wiki in more than 4 editions.
def users_active_more_than_4_editions(data, index):
    return users_active_more_than_x_editions(data, index, 5)


# this metric gets, per month, those users who have contributed to the wiki in more than 24 editions.
def users_active_more_than_24_editions(data, index):
    return users_active_more_than_x_editions(data, index, 25)


# this metric gets, per month, those users who have contributed to the wiki in more than 99 editions.
def users_active_more_than_99_editions(data, index):
    return users_active_more_than_x_editions(data, index, 100)


########################################################################

# RATIOS

##### Helper functions #####


def anonymous_edits(data, index):
    series = data[data['contributor_name'] == 'Anonymous']
    series = series.groupby(pd.Grouper(key='timestamp', freq='MS')).size()
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series


##### callable ditribution metrics #####


def edits_per_users_accum(data, index):
    return (edits_accum(data, index) / users_accum(data, index))


def edits_per_users_monthly(data, index):
    return (edits(data, index) / users_active(data, index))


def edits_in_articles_per_users_accum(data, index):
    return (edits_main_content_accum(data, index) / users_accum(data, index))


def edits_in_articles_per_users_monthly(data, index):
    return (edits_main_content(data, index) / users_active(data, index))


def edits_per_pages_accum(data, index):
    return (edits_accum(data, index) / pages_accum(data, index))


def edits_per_pages_monthly(data, index):
    return (edits(data, index) / pages_edited(data, index))


def percentage_edits_by_anonymous_monthly(data, index):
    series_anon_edits = anonymous_edits(data, index)
    series_total_edits = edits(data, index)
    series = series_anon_edits / series_total_edits
    series *= 100 # we want it to be displayed in percentage
    return series


def percentage_edits_by_anonymous_accum(data, index):
    series_anon_edits_accum = anonymous_edits(data, index).cumsum()
    series_total_edits_accum = edits_accum(data, index)
    series = series_anon_edits_accum / series_total_edits_accum
    series *= 100 # we want it to be displayed in percentage
    return series


########################################################################

# Distribution Of Work

##### Helper functions #####


def contributions_per_author(data):
    """
    Takes data and outputs data grouped by its author
    """
    return data.groupby('contributor_id').size()


def calc_ratio_percentile_max(data, index, percentile, minimal_users):
    return calc_ratio_percentile(data, index, 1, percentile, minimal_users)


def calc_ratio_percentile(data, index, top_percentile, percentile, minimal_users):

    # Note that contributions is an *unsorted* list of contributions per author
    def ratio_max_percentile_for_period(contributions, percentage):

        position = int(n_users * percentage)

        # get top users until user who corresponds to percentil n
        top_users = contributions.nlargest(position)

        # get top user and percentil n user
        p_max = top_users[top_percentile-1]
        percentile = top_users[-1]

        # calculate ratio between percentiles
        return p_max / percentile

    percentage = percentile * 0.01
    i = 0
    monthly_data = data.groupby(pd.Grouper(key='timestamp', freq='MS'))
    result = pd.Series(index=monthly_data.size().index)
    indices = result.index
    accum_data = pd.DataFrame()
    for name, group in monthly_data:
        # Accumulate data so far
        accum_data = accum_data.append(group)

        # Get contributions per contributor
        contributions = contributions_per_author(accum_data)

        n_users = len(contributions)

        # Skip when the wiki has too few users
        if n_users < minimal_users:
            result[indices[i]] = np.NaN
        else:
            result[indices[i]] = ratio_max_percentile_for_period(contributions, percentage)
        i = i + 1

    return result

##### callable ditribution metrics #####


def gini_accum(data, index):

    #~ data = raw_data.set_index([raw_data['timestamp'].dt.to_period('M'), raw_data.index])
    monthly_data = data.groupby(pd.Grouper(key='timestamp', freq='MS'))
    if index is not None:
        gini_accum_df = pd.Series(index=index)
    else:
        gini_accum_df = pd.Series(index=monthly_data.size().index)
    indices = gini_accum_df.index
    i = 0
    accum_data = pd.DataFrame()
    for name, group in monthly_data:
        # Accumulate data so far
        accum_data = accum_data.append(group)

        # Get contributions per contributor, sort them
        #   and make it a list to call to gini_coeff()
        values = contributions_per_author(accum_data) \
                .tolist()

        n_users = len(values)

        if (n_users) < MINIMAL_USERS_GINI:
            gini_accum_df[indices[i]] = np.NaN
        else:
            gini_accum_df[indices[i]] = ineq.gini_corrected(values, n_users)
        i = i + 1

    return gini_accum_df


def ratio_percentiles_max_5(data, index):
    return calc_ratio_percentile_max(data,index, 5,
                    MINIMAL_USERS_PERCENTIL_MAX_5)


def ratio_percentiles_max_10(data, index):
    return calc_ratio_percentile_max(data, index, 10,
                    MINIMAL_USERS_PERCENTIL_MAX_10)


def ratio_percentiles_max_20(data, index):
    return calc_ratio_percentile_max(data, index, 20,
                    MINIMAL_USERS_PERCENTIL_MAX_20)


def ratio_percentiles_5_10(data, index):
    return calc_ratio_percentile(data, index, 5, 10,
                    MINIMAL_USERS_PERCENTIL_5_10)


def ratio_percentiles_10_20(data, index):
    return calc_ratio_percentile(data, index, 10, 20,
                    MINIMAL_USERS_PERCENTIL_10_20)


def ratio_10_90(data, index):
    i = 0
    monthly_data = data.groupby(pd.Grouper(key='timestamp', freq='MS'))
    result = pd.Series(index=monthly_data.size().index)
    indices = result.index
    accum_data = pd.DataFrame()
    for name, group in monthly_data:
        # Get contributions per contributor, sort them
        #   and make it a Python list
        accum_data = accum_data.append(group)
        contributions = contributions_per_author(accum_data)

        n_users = len(contributions)

        # Skip when the wiki has too few users
        if n_users < MINIMAL_USERS_RATIO_10_90:
            result[indices[i]] = np.NaN
        else:
            result[indices[i]] = ineq.ratio_top10_rest(contributions)
        i = i + 1

    return result

