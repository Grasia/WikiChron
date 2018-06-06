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
import powerlaw
import math

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


def apply_time_series(data, index, fun):
    monthly_data = data.groupby(pd.Grouper(key='timestamp', freq='MS'))
    series = monthly_data.apply(lambda x: fun(x))
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series


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


def users_active(data, index):
    monthly_data = data.groupby(pd.Grouper(key='timestamp', freq='MS'))
    series = monthly_data.apply(lambda x: len(x.contributor_id.unique()))
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series


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

def power_law_alpha_calc(data):
    try:
        contribs = np.array(contributions_per_author(data))
        if (len(contribs) == 0):
            return np.nan
        r = powerlaw.Fit(contribs, discrete=True)
        return r.power_law.alpha
    except:
        return np.nan

##### callable ditribution metrics #####


def gini_accum(data, index):

    def gini_coeff(values):
        """
        Extracted from wikixray/graphics.py:70
        Plots a GINI graph for author contributions

        @type  values: list of ints
        @param values: list of integers summarizing total contributions for each registered author
        """

        n_users = len(values) # n_users => n + 1
        if (n_users) < MINIMAL_USERS_GINI:
            return np.NaN

        sum_numerator=0
        sum_denominator=0
        for i in range(1, n_users):
            sum_numerator += (n_users-i) * values[i]
            sum_denominator += values[i]
        if sum_denominator == 0:
            return np.NaN
        ## Apply math function for the Gini coefficient
        g_coeff = n_users-2*(sum_numerator/sum_denominator)
        ## Now, apply Deltas, 2003 correction for small datasets:
        g_coeff *= (1.0 / (n_users - 2))
        return g_coeff

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
                .sort_values(ascending=True) \
                .tolist()
        gini_accum_df[indices[i]] = gini_coeff(values)
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

    # contributions is a *sorted* list of contributions per author
    #   in an descending order (from most contributions to less contributions)
    def ratio_top_rest_for_period(contributions, percentage_top):
        top_percent_users = math.ceil(n_users * percentage_top);
        #~ rest_users = floor(n_users * (1 - percentage_top));
        edits_top = contributions[:top_percent_users].sum()
        edits_rest = contributions[top_percent_users:].sum()

        return edits_top / edits_rest


    percentage = 10 * 0.01
    i = 0
    monthly_data = data.groupby(pd.Grouper(key='timestamp', freq='MS'))
    result = pd.Series(index=monthly_data.size().index)
    indices = result.index
    accum_data = pd.DataFrame()
    for name, group in monthly_data:
        # Get contributions per contributor, sort them
        #   and make it a Python list
        accum_data = accum_data.append(group)
        contributions = contributions_per_author(accum_data) \
                .sort_values(ascending=False)

        n_users = len(contributions)

        # Skip when the wiki has too few users
        if n_users < MINIMAL_USERS_RATIO_10_90:
            result[indices[i]] = np.NaN
        else:
            result[indices[i]] = ratio_top_rest_for_period(contributions,
                                                            percentage)
        i = i + 1

    return result


def power_law_alpha(data, index):
    return apply_time_series(data, index, power_law_alpha_calc)
