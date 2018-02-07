#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   stats.py

   Descp:

   Created on: 14-nov-2017

   Copyright 2017 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

import pandas as pd
import numpy as np

# CONSTANTS
MINIMAL_USERS_PERCENTIL_MAX_5 = 100



# Mandatory to run before to calculate any stats!!
# TOREDESIGN & TOIMPROVE!
# deprecated
#~ def init_stats(data):
    #~ global index;
    #~ monthly_data = data.groupby(pd.Grouper(key='timestamp',freq='MS'))
    #~ index = monthly_data.size().index

def calculate_index_all_months(data):
    monthly_data = data.groupby(pd.Grouper(key='timestamp',freq='MS'))
    index = monthly_data.size().index
    return index

# Pages

def pages_new(data, index):
    # We use the fact that data is sorted first by page_title and them by revision_id
    # If we drop publicates we will get the first revision for each page_title, which
    #  corresponds with the date it was created.
    pages = data.drop_duplicates('page_id')
    series = pages.groupby(pd.Grouper(key='timestamp',freq='MS')).size()
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series

def pages_accum(data, index):
    return (pages_new(data, index).cumsum())

def pages_main_new(data, index):
    pages = data.drop_duplicates('page_id')
    main_pages = pages[pages['page_ns'] == 0]
    series = main_pages.groupby(pd.Grouper(key='timestamp',freq='MS')).size()
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series

def pages_main_accum(data, index):
    return (pages_main_new(data, index).cumsum())

def pages_edited(data, index):
    monthly_data = data.groupby([pd.Grouper(key='timestamp',freq='MS')])
    series = monthly_data.apply(lambda x: len(x.page_id.unique()))
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series

def main_edited(data, index):
    main_pages = data[data['page_ns'] == 0]
    monthly_data = main_pages.groupby([pd.Grouper(key='timestamp',freq='MS')])
    series = monthly_data.apply(lambda x: len(x.page_id.unique()))
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series

########################################################################

# Editions

def edits(data, index):
    monthly_data = data.groupby(pd.Grouper(key='timestamp',freq='MS'))
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

def users_active(data, index):
    monthly_data = data.groupby(pd.Grouper(key='timestamp',freq='MS'))
    series = monthly_data.apply(lambda x: len(x.contributor_id.unique()))
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series

def users_new(data, index):
    users = data.drop_duplicates('contributor_id')
    series = users.groupby(pd.Grouper(key='timestamp',freq='MS')).size()
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series

def users_accum(data, index):
    return (users_new(data, index).cumsum())

def users_new_anonymous(data, index):
    users = data.drop_duplicates('contributor_id')
    anonymous_users = users[users['contributor_name'] == 'Anonymous']
    series = anonymous_users.groupby(pd.Grouper(key='timestamp',freq='MS')).size()
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series

def users_anonymous_accum(data, index):
    return (users_new_anonymous(data, index).cumsum())

def users_new_registered(data, index):
    users = data.drop_duplicates('contributor_id')
    non_anonymous_users = users[users['contributor_name'] != 'Anonymous']
    series =  non_anonymous_users.groupby(pd.Grouper(key='timestamp',freq='MS')).size()
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series

def users_registered_accum(data, index):
    return (users_new_registered(data, index).cumsum())

########################################################################

# Ratios

def edits_per_users_accum(data, index):
    return (edits_accum(data, index) / users_accum(data, index))

def edits_per_users_monthly(data, index):
    return (edits(data, index) / users_active(data, index))

def edits_per_pages_accum(data, index):
    return (edits_accum(data, index) / pages_accum(data, index))

def edits_per_pages_monthly(data, index):
    return (edits(data, index) / pages_edited(data, index))

########################################################################

# Helper functions

def contributions_per_author(data):
    """
    Takes data and outputs data grouped by its author
    """
    return data.groupby('contributor_id').size()

global stats_period, contribution;
stats_period = 'M'; # format has to follow the frequency p
contribution = 'revision'

def init_stats(raw_data):
    """
    Here we're gonna format the data in periods and contributions.
    What is defined as period and what is defined as contribution has to
      be defined beforehand
    This function must be called before to make any metric calculations.
    Otherwise the data would be in an unexpected format.
    The ouput will be a dataframe indexed by a PeriodIndex.
    """
    if contribution == 'revision':
        data = raw_data.set_index([raw_data['timestamp'].dt.to_period(stats_period), raw_data.revision_id])
        data = data.sort_index(level=0)
    else:
        data = raw_data.copy()
    data.index.set_names(['period', 'id'], inplace=True)
    return data

########################################################################

# Inequality

def gini_accum(data, index):

    def gini_coeff(values):
        """
        Extracted from wikixray/graphics.py:70
        Plots a GINI graph for author contributions

        @type  values: list of ints
        @param values: list of integers summarizing total contributions for each registered author
        """
        sum_numerator=0
        sum_denominator=0
        for i in range(1, len(values)):
            sum_numerator += (len(values)-i) * values[i]
            sum_denominator += values[i]
        if sum_denominator == 0:
            return np.NaN
        ## Apply math function for the Gini coefficient
        g_coeff= (1.0/(len(values)-1))*(len(values)-2*(sum_numerator/sum_denominator))
        return g_coeff

    #~ import pdb; pdb.set_trace()
    #~ data = raw_data.set_index([raw_data['timestamp'].dt.to_period('M'), raw_data.index])
    monthly_data = data.groupby(pd.Grouper(key='timestamp',freq='MS'))
    gini_accum_df = pd.Series(index=monthly_data.size().index)
    indices = gini_accum_df.index
    i = 0
    for name, group in monthly_data:
        # Get contributions per contributor, sort them
        #   and make it a list to call to gini_coeff()
        values = contributions_per_author(group) \
                .sort_values(ascending=True) \
                .tolist()
        gini_accum_df[indices[i]] = gini_coeff(values)
        i = i + 1

    if index is not None:
        gini_accum_df = gini_accum_df.reindex(index, fill_value=0)

    return gini_accum_df


def ratio_percentiles_max_5(raw_data, index):
    data = init_stats(raw_data)

    period_index = data.index.get_level_values('period').unique()
    result_time_series = pd.Series(index = period_index)
    for period in period_index:

        # Get contributions per contributor (unsorted)
        # use accumulated data until period i
        contributions = contributions_per_author(data[:period])
        n_users = len(contributions)
        percentil_5 = int(n_users * 0.05)

        # Skip when the wiki has too few users
        if n_users < MINIMAL_USERS_PERCENTIL_MAX_5:
            result_time_series[period] = np.NaN
            continue

        # get top users until user who corresponds to percentil 5
        top_users = contributions.nlargest(percentil_5)

        # get top user and percentil 5 user
        p_max = top_users[0]
        p_5 = top_users[-1]

        # calculate ratio between percentiles
        result = p_max / p_5

        result_time_series[period] = result

    return result_time_series


def ratio_percentiles_1_5(raw_data, index):
    data = init_stats(raw_data)
