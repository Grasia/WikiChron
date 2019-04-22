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
from dateutil.relativedelta import relativedelta


def calculate_index_all_months(data):
    monthly_data = data.groupby(pd.Grouper(key='timestamp', freq='MS'))
    index = monthly_data.size().index
    return index



# Users


###### Helper Functions ######

#### Helper metric users active ####

def users_active_more_than_x_editions(data, index, x):
    monthly_edits = data.groupby([pd.Grouper(key='timestamp', freq='MS'), 'contributor_name']).size()
    monthly_edits_filtered = monthly_edits[monthly_edits > x].to_frame(name='pages_edited').reset_index()
    series = monthly_edits_filtered.groupby(pd.Grouper(key='timestamp', freq='MS')).size()
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series

#### Helper metric 2 ####

def add_x_months(data, months):
    return data['timestamp'].apply(lambda x: x + relativedelta(months = +months))

def displace_x_months_per_user(data, months):
    return data.shift(months)

def current_streak_x_or_y_months_in_a_row(data, index, z, y):
    mothly = data.groupby(['contributor_id',pd.Grouper(key = 'timestamp', freq = 'MS')]).size().to_frame('prueba').reset_index()
    mothly['add_months'] = add_x_months(mothly, z)
    lista = ['contributor_id']
    lista.append('add_months')
    if y > 0:
      mothly['add_y_months'] = add_x_months(mothly, y)
      lista.append('add_y_months')
    group_users = mothly[lista].groupby(['contributor_id'])
    displace_z_month = displace_x_months_per_user(group_users['add_months'], z)
    mothly['displace']= displace_z_month
    if y > 0:
      displace_y_month = displace_x_months_per_user(group_users['add_y_months'], y)
      mothly['displace_y_month']= displace_y_month
      current_streak = mothly[(mothly['displace'] == mothly['timestamp']) & (mothly['displace_y_month'] != mothly['timestamp'])]
    elif z == 1:
      current_streak = mothly[mothly['displace'] != mothly['timestamp']]
    elif z == 6:
      current_streak = mothly[mothly['displace'] == mothly['timestamp']]
    series = current_streak.groupby(pd.Grouper(key = 'timestamp', freq = 'MS')).size()
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series


#### Helper metric 3 ####

# this function is a helper for the functions in the metric 3 section: it filters the editors according to a condition which depends on the numbers x and y, passed as parameters by the caller functions.
def filter_users_first_edition(data, index, x, y):
# 1) Get the index of the dataframe to analyze: it must include all the months recorded in the history of the wiki.
    new_index = data.groupby(pd.Grouper(key='timestamp', freq='MS')).size().to_frame('months').index
# 2) create a dataframe in which we have the cumulative sum of the editions the user has made all along the history of the wiki.
    users_month_edits =data.groupby(['contributor_id']).apply(lambda x: x.groupby(pd.Grouper(key='timestamp', freq='MS')).size().to_frame('nEdits').reindex(new_index, fill_value=0).cumsum()).reset_index()
# 3) add a new column to the dataframe ('position') in which the number of each row depending on the contributor ID is computed: note that the count isn't restarted until nEdits > 0.
    cond = users_month_edits['nEdits'] == 0
    users_month_edits['position'] = np.where(cond, 0, users_month_edits.groupby([cond, 'contributor_id']).cumcount() + 1)

    if y > 0:
        condition = ((users_month_edits['position'] >= x) & (users_month_edits['position'] <= y)) & (users_month_edits['nEdits'] != users_month_edits['nEdits'].shift())
    else:
        condition = (users_month_edits['position'] > x) & (users_month_edits['nEdits'] != users_month_edits['nEdits'].shift())

    users_month_edits['included'] = np.where(condition, 1,0)
# 4) count the number of appereances each timestamp has in the 'included' column:
    series = pd.Series(users_month_edits.groupby(['timestamp']).sum()['included'], new_index)
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series


#### Helper metric 4 ####

# this function is a helper for the functions in the metric 4 section: it filters the editors according to a condition which depends on the number x , passed as parameter by the caller functions.
def filter_users_last_edition(data, index, x):
# 1) Get the index of the dataframe to analyze: it must include all the months recorded in the history of the wiki.
    new_index = data.groupby(pd.Grouper(key='timestamp', freq='MS')).size().to_frame('months').index
# 2) create a dataframe in which we have the cumulative sum of the editions the user has made all along the history of the wiki.
    users_month_edits =data.groupby(['contributor_id']).apply(lambda x: x.groupby(pd.Grouper(key='timestamp', freq='MS')).size().to_frame('nEdits').reindex(new_index, fill_value=0).cumsum()).reset_index()
# 3) add a new column to the dataframe ('position') in which the number of each row depending grouping by contributor ID is computed: note that the count isn't restarted until nEdits > 0.
    cond = users_month_edits['nEdits'] == 0
    users_month_edits['position'] = np.where(cond, 0, users_month_edits.groupby([cond, 'contributor_id', 'nEdits']).cumcount() + 1)
# 4) add a new column, 'included', which will contain two possible values: 0 if the user didn't edit in month X or edited in month X but not in months specified by caller function, and 1 if the user edited in month X and made his last edition in month X-1

    if x != 6:
        cond1 = ((users_month_edits['position'] == 1) & (users_month_edits['position'].shift() == x)) & (users_month_edits['contributor_id'] == users_month_edits['contributor_id'].shift())
    else:
        cond1 = ((users_month_edits['position'] == 1) & (users_month_edits['position'].shift() > x)) & (users_month_edits['contributor_id'] == users_month_edits['contributor_id'].shift())

    users_month_edits['included'] = np.where(cond1, 1, 0)
# 5) create series
    series = pd.Series(users_month_edits.groupby(['timestamp']).sum()['included'], new_index)
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series



#### Helper metric 5 ####

# this helper functions filters the editors according to their number of editions, which can be in a range: [x, y] or >=x, with x and y specified by the caller functions
def filter_users_number_of_edits(data, index, x, y):
# 1) Get the index of the dataframe to analyze: it must include all the months recorded in the history of the wiki.
    new_index = data.groupby(pd.Grouper(key='timestamp', freq='MS')).size().to_frame('months').index
# 2) create a dataframe in which we have the cumulative sum of the editions the user has made all along the history of the wiki.
    users_month_edits =data.groupby(['contributor_id']).apply(lambda x: x.groupby(pd.Grouper(key='timestamp', freq='MS'))
                                                        .size().to_frame('nEdits').reindex(new_index, fill_value=0).cumsum()).reset_index()
# 3) add a new column to the dataframe ('included') in which 2 values are possible: 1. if the user has made between >=x and <=y editions in month x - 1 (shift function is used to access the previous row), a 1 appears. 2. Otherwise, the value in the 'included' column will be 0.

    if y != 0:
        cond1 = (users_month_edits['contributor_id'].shift() == users_month_edits['contributor_id']) & (users_month_edits['nEdits'] != users_month_edits['nEdits'].shift()) & ((users_month_edits['nEdits'].shift()<=x) & (users_month_edits['nEdits'].shift()>=y))
    else:
        cond1 = (users_month_edits['contributor_id'].shift() == users_month_edits['contributor_id']) & (users_month_edits['nEdits'] != users_month_edits['nEdits'].shift()) & (users_month_edits['nEdits'].shift()>=x)

    users_month_edits['included'] = np.where(cond1, 1, 0)
    series = pd.Series(users_month_edits.groupby(['timestamp']).sum()['included'], new_index)
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series


#### Helper metrics 9 and 10 ####

# this helper function gets the number of users that have edited a particular kind of page, specified by the parameter page_ns
def filter_users_pageNS(data, index, page_ns):
    edits_page = data[data['page_ns'] == page_ns]
    series = edits_page.groupby(pd.Grouper(key = 'timestamp', freq = 'MS'))['contributor_id'].nunique()
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series


#### Helper metrics to calculate the number of edits and the percentage of edits done by user categories ####

#this function calculates the number of editions done on each month by each user category (users that are new to the wiki, users that have done between 1 and 4, 5 and 24, 25 and 99 and more or equal to 100 editions in all the history of the wiki)
def number_of_edits_by_user_category(data, index, x, y):
# 1) Get the index of the dataframe to analyze: it must include all the months recorded in the history of the wiki.
    new_index = data.groupby(pd.Grouper(key='timestamp', freq='MS')).size().to_frame('months').index
# 2) create a dataframe in which we have the cumulative sum of the editions the user has made all along the history of the wiki.
    users_month_edits =data.groupby(['contributor_id']).apply(lambda x: x.groupby(pd.Grouper(key='timestamp', freq='MS')).size().to_frame('nEdits').reindex(new_index, fill_value=0).cumsum()).reset_index()
# 3) add a new column, edits_per_month, which is equal to the substraction of the number of edits in month X minus the number of edits in month X-1
    cond = (users_month_edits['contributor_id'] == users_month_edits['contributor_id'].shift())
    users_month_edits['nEdits_per_month'] = np.where(cond, users_month_edits['nEdits'] - users_month_edits['nEdits'].shift(), users_month_edits['nEdits'])
# 4) add a new column to the dataframe ('included') in which 2 values are possible: 1. if the user has made between >=x and <=y editions in month x - 1 (shift function is used to access the previous row), a 1 appears. 2. Otherwise, the value in the 'included' column will be 0.
    if (y != 0) and (x > 0):
        cond1 = (users_month_edits['contributor_id'].shift() == users_month_edits['contributor_id']) & (users_month_edits['nEdits'] != users_month_edits['nEdits'].shift()) & ((users_month_edits['nEdits'].shift()<=x) & (users_month_edits['nEdits'].shift()>=y))
    elif (y == 0) and (x == 0):
        cond1 = (((users_month_edits['nEdits'] > 0) & (users_month_edits['nEdits'].shift() == 0)) & (users_month_edits['contributor_id'] == users_month_edits['contributor_id'].shift())) | ((users_month_edits['contributor_id'] != users_month_edits['contributor_id'].shift()) & (users_month_edits['nEdits'] > 0))
    else:
        cond1 = (users_month_edits['contributor_id'].shift() == users_month_edits['contributor_id']) & (users_month_edits['nEdits'] != users_month_edits['nEdits'].shift()) & (users_month_edits['nEdits'].shift()>=x)
    users_month_edits['included'] = np.where(cond1, 1, 0)
    # 5) we want to get the total number of edits done by all the users in a group, by timestamp: calculate how many edits were done by the users included in the group, and by the users not included in the group
    num_edits_of_groups = users_month_edits.groupby([pd.Grouper(key ='timestamp', freq='MS'),'included'])['nEdits_per_month'].sum().reset_index(name='nEditsgroup')
    return num_edits_of_groups

#this function calculates the percentage of editions done on each month by each user category (users that are new to the wiki, users that have done between 1 and 4, 5 and 24, 25 and 99 and more or equal to 100 editions in all the history of the wiki)
def percentage_of_edits_by_user_category(data, index, x, y):
    num_edits_of_groups = number_of_edits_by_user_category(data, index, x, y)
    num_edits_of_groups['total_edits'] = num_edits_of_groups.groupby(pd.Grouper(key ='timestamp', freq='MS'))['nEditsgroup'].transform(sum)
    cond = (num_edits_of_groups['included'] == 1)
    percentage_of_edits_group = np.where(cond, (num_edits_of_groups['nEditsgroup'].div(num_edits_of_groups['total_edits']) * 100), 0)
    percentage_edits_group_per_month = pd.DataFrame({'timestamp': num_edits_of_groups['timestamp'], 'n_edits': percentage_of_edits_group}).groupby(pd.Grouper(key='timestamp', freq='MS')).sum().reset_index()
    series = percentage_edits_group_per_month.set_index('timestamp')['n_edits'].rename_axis(None)
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series

###### Callable Functions ######

############################ METRIC 1: USERS NEW AND USERS REINCIDENT ###############################################################

def users_new(data, index):
    users = data.drop_duplicates('contributor_id')
    series = users.groupby(pd.Grouper(key='timestamp', freq='MS')).size()
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series

#users who make their second edition in the wiki (we want the count for this kind of users per month)
def users_reincident(data, index):
    data['test_duplicated'] = data['contributor_id'].duplicated()
    data = data[data['contributor_name'] != 'Anonymous']
    users_reincident = data[data['test_duplicated'] == True]
#determine in which month each user performed their second edition-> can be the same month as the first one
#1) get number of editions per month for every user
    users_reincident = users_reincident.groupby(['contributor_id', pd.Grouper(key='timestamp', freq='MS')]).size().to_frame('edits_count').reset_index()
#2) get the accum. number of edits per user each month
    users_reincident['accum_edit_count'] = users_reincident.groupby('contributor_id')['edits_count'].transform(lambda x: x.cumsum())
#3) drop rows in which the accum_edit_count is less than 2
    users_reincident = users_reincident[users_reincident['accum_edit_count'] > 1]
#4) now, we just want the first month in which the user became reincident: (drop_duplicates drops all rows but first, so as it is sorted, for sure we will keep the first month)
    users_reincident = users_reincident.drop_duplicates('contributor_id')
#5) group by timestamp and get the count of reincident users per month
    series = users_reincident.groupby(pd.Grouper(key='timestamp', freq='MS')).size()
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series


############################ METRIC 2 #################################################################################################

def current_streak_this_month(data, index):
    return current_streak_x_or_y_months_in_a_row(data, index, 1, 0)
    

def current_streak_2_or_3_months_in_a_row(data, index):
    return current_streak_x_or_y_months_in_a_row(data, index, 1, 3)
    


def current_streak_4_or_6_months_in_a_row(data, index):
    return current_streak_x_or_y_months_in_a_row(data, index, 3, 6)
    


def current_streak_more_than_six_months_in_a_row(data, index):
    return current_streak_x_or_y_months_in_a_row(data, index, 6, 0)
    

def current_streak(data, index):
    this_month = current_streak_this_month(data, index)
    two_three_months = current_streak_2_or_3_months_in_a_row(data, index)
    four_six_months = current_streak_4_or_6_months_in_a_row(data, index)
    more_six = current_streak_more_than_six_months_in_a_row(data, index)
    this_month.name = 'this months'
    two_three_months.name = 'between two and three months in a row'
    four_six_months.name = 'between four and six months in a row'
    more_six.name = 'more than six months in a row'
    return [this_month, two_three_months, four_six_months, more_six]

############################ METRIC 3 #################################################################################################

# this metric counts the users whose first edition was between 1 and 3 months ago:
def users_first_edit_between_1_3_months_ago(data, index):
    return filter_users_first_edition(data, index, 2, 4)

# this metric counts the users whose first edition was between 4 and 6 months ago:
def users_first_edit_between_4_6_months_ago(data, index):
    return filter_users_first_edition(data, index, 5, 7)

# this metric counts the users whose first edition is more than 6 months old:
def users_first_edit_more_than_6_months_ago(data, index):
    return filter_users_first_edition(data, index, 7, 0)

def users_first_edit(data, index):
    this_month = users_new(data, index)
    one_three = users_first_edit_between_1_3_months_ago(data, index)
    four_six = users_first_edit_between_4_6_months_ago(data, index)
    more_six = users_first_edit_more_than_6_months_ago(data, index)
    this_month.name ='this month'
    one_three.name = 'between 1 and 3 months ago'
    four_six.name = 'between 4 and 6 months ago'
    more_six.name = 'more than 6 months ago'
    return [this_month, one_three, four_six, more_six]
############################ METRIC 4 #################################################################################################

# This metric counts, among the users that have edited in that month X, the ones that have edited the last time in month X-1
def users_last_edit_1_month_ago(data, index):
    return filter_users_last_edition(data, index, 1)

# This metric counts, among the users that have edited in month X, which ones have edited the last time in month X-2 or X-3
def users_last_edit_2_or_3_months_ago(data, index):
    return filter_users_last_edition(data, index, 2)

# This metric counts, per each month X, among the users that have edited in that month X, the ones that have edited the last time in month X-4, X-5 or X-6
def users_last_edit_4_or_5_or_6_months_ago(data, index):
    return filter_users_last_edition(data, index, 4)

# This metric counts, per each month X, among the users that have edited in that month X, the ones that have edited the last time in any month > X-6
def users_last_edit_more_than_6_months_ago(data, index):
    return filter_users_last_edition(data, index, 6)

def users_last_edit(data, index):
    this_month = users_new(data, index)
    one_month = users_last_edit_1_month_ago(data, index)
    two_three_months = users_last_edit_2_or_3_months_ago(data, index)
    four_six_months = users_last_edit_4_or_5_or_6_months_ago(data, index)
    more_six_months = users_last_edit_more_than_6_months_ago(data, index)
    this_month.name = 'this month'
    one_month.name = '1 month ago'
    two_three_months.name = 'between 2 and 3 months ago'
    four_six_months.name = 'between 4 and 6 months ago'
    more_six_months.name = 'more than six months ago'
    return [this_month, one_month, two_three_months, four_six_months, more_six_months]

############################ METRIC 5 #################################################################################################

# In this metric, we want to get, among the users that make an edition in month X, which ones have done n editions, with n in [1,4], until month X-1
def users_number_of_edits_between_1_and_4(data, index):
    return filter_users_number_of_edits(data, index, 4, 1)

# In this metric, we want to get, among the users that make an edition in month X, which ones have done n editions, with n in [5,24], until month X-1
def users_number_of_edits_between_5_and_24(data, index):
    return filter_users_number_of_edits(data, index, 24, 5)

# In this metric, we want to get, among the users that make an edition in month X, which ones have done n editions, with n in [25,99], until month X-1
def users_number_of_edits_between_25_and_99(data, index):
    return filter_users_number_of_edits(data, index, 99, 25)

# In this metric, we want to get, among the users that make an edition in month X, which ones have done n editions, with n>=100, until month X-1
def users_number_of_edits_highEq_100(data, index):
    return filter_users_number_of_edits(data, index, 100, 0)

def users_number_of_edits(data, index):
    one_four = users_number_of_edits_between_1_and_4(data, index)
    between_5_24 = users_number_of_edits_between_5_and_24(data, index)
    between_25_99 = users_number_of_edits_between_25_and_99(data, index)
    highEq_100 = users_number_of_edits_highEq_100(data, index)
    one_four.name = 'between 1 and 4'
    between_5_24.name = 'between 5 and 24'
    between_25_99.name = 'between 25 and 99'
    highEq_100.name = 'more than 100'
    return [one_four, between_5_24, between_25_99, highEq_100]

def users_number_of_edits_abs(data, index):
    one_four = users_number_of_edits_between_1_and_4(data, index).to_frame('one_four')
    between_5_24 = users_number_of_edits_between_5_and_24(data, index).to_frame('5_24')
    between_25_99 = users_number_of_edits_between_25_and_99(data, index).to_frame('25_99')
    highEq_100 = users_number_of_edits_highEq_100(data, index).to_frame('highEq_100')
    concatenate = pd.concat([one_four, between_5_24, between_25_99, highEq_100], axis = 1)
    concatenate['suma'] = concatenate[['one_four', '5_24', '25_99', 'highEq_100']].sum(axis=1)
    concatenate['one_four'] = (concatenate['one_four']/concatenate['suma'])*100
    concatenate['5_24'] = (concatenate['5_24']/concatenate['suma'])*100
    concatenate['25_99'] = (concatenate['25_99']/concatenate['suma'])*100
    concatenate['highEq_100'] = (concatenate['highEq_100']/concatenate['suma'])*100
    one_four = pd.Series(concatenate['one_four'], index = concatenate.index)
    between_5_24 = pd.Series(concatenate['5_24'], index = concatenate.index)
    between_25_99 = pd.Series(concatenate['25_99'], index = concatenate.index)
    highEq_100 = pd.Series(concatenate['highEq_100'], index = concatenate.index)
    one_four.name = 'between 1 and 4'
    between_5_24.name = 'between 5 and 24'
    between_25_99.name = 'between 25 and 99'
    highEq_100.name = 'more than 100'
    return [one_four, between_5_24, between_25_99, highEq_100]
############################ METRICS 9 and 10 #################################################################################################

#this metric filters how many users have edited a main page
def users_main_page(data, index):
  return filter_users_pageNS(data, index, 0)

#this metric filters how many users have edited a template page
def users_template_page(data, index):
   return filter_users_pageNS(data, index, 10)

#this metric filters how many users have edited a talk page
def talk_page_users(data,index):
    return filter_users_pageNS(data, index, 3)

def type_page_users_edit(data, index):
    main_page = users_main_page(data, index)
    template_page = users_template_page(data, index)
    talk_page = talk_page_users(data,index)
    main_page.name = 'main_page'
    template_page.name = 'template_page'
    talk_page.name = 'talk_page'
    return [main_page, template_page, talk_page]

############################ METRICS TO CALCULATE THE PARTICIPATION LEVEL OF DIFFERENT USER CATEGORIES #########################################

### 1) NUMBER OF EDITIONS PER USER CATEGORY EACH MONTH ###

#this metric gets the total number of editions per month that were done by users ho have made between 1 and 4 editions in all the history of the wiki
def number_of_edits_by_beginner_users(data, index):
    num_edits_of_groups = number_of_edits_by_user_category(data, index, 4, 1) 
# 1) we only want to know how many edits were done by the included users
    cond = (num_edits_of_groups['included'] == 1)
    edits_group_final = np.where(cond, num_edits_of_groups['nEditsgroup'], 0)
    num_edits_group_per_month = pd.DataFrame({'timestamp': num_edits_of_groups['timestamp'], 'n_edits': edits_group_final})
# 2) It is possible that the same month is repeated twice in the dataframe: 1. for the not included users (in which the n_edits column will always have a value of 0), 2. For the included users, in which the value of the n_edits column will be = number of edits done by the users in the category
    num_edits_group_per_month = num_edits_group_per_month.groupby(pd.Grouper(key='timestamp', freq='MS')).sum().reset_index()
    series = num_edits_group_per_month.set_index('timestamp')['n_edits'].rename_axis(None)
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series

#this metric gets the total number of editions per month that were done by users ho have made between 5 and 24 editions in all the history of the wiki
def number_of_edits_by_advanced_users(data, index):
    num_edits_of_groups = number_of_edits_by_user_category(data, index, 24, 5) 
# 1) we only want to know how many edits were done by the included users
    cond = (num_edits_of_groups['included'] == 1)
    edits_group_final = np.where(cond, num_edits_of_groups['nEditsgroup'], 0)
    num_edits_group_per_month = pd.DataFrame({'timestamp': num_edits_of_groups['timestamp'], 'n_edits': edits_group_final})
# 2) It is possible that the same month is repeated twice in the dataframe: 1. for the not included users (in which the n_edits column will always have a value of 0), 2. For the included users, in which the value of the n_edits column will be = number of edits done by the users in the category
    num_edits_group_per_month = num_edits_group_per_month.groupby(pd.Grouper(key='timestamp', freq='MS')).sum().reset_index()
    series = num_edits_group_per_month.set_index('timestamp')['n_edits'].rename_axis(None)
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series

#this metric gets the total number of editions per month that were done by users ho have made between 25 and 99 editions in all the history of the wiki
def number_of_edits_by_experimented_users(data, index):
     num_edits_of_groups = number_of_edits_by_user_category(data, index, 99, 25) 
# 1) we only want to know how many edits were done by the included users
     cond = (num_edits_of_groups['included'] == 1)
     edits_group_final = np.where(cond, num_edits_of_groups['nEditsgroup'], 0)
     num_edits_group_per_month = pd.DataFrame({'timestamp': num_edits_of_groups['timestamp'], 'n_edits': edits_group_final})
# 2) It is possible that the same month is repeated twice in the dataframe: 1. for the not included users (in which the n_edits column will always have a value of 0), 2. For the included users, in which the value of the n_edits column will be = number of edits done by the users in the category
     num_edits_group_per_month = num_edits_group_per_month.groupby(pd.Grouper(key='timestamp', freq='MS')).sum().reset_index()
     series = num_edits_group_per_month.set_index('timestamp')['n_edits'].rename_axis(None)
     if index is not None:
         series = series.reindex(index, fill_value=0)
     return series

#this metric gets the total number of editions per month that were done by users ho have made more or equal to 100 editions in all the history of the wiki
def number_of_edits_by_highly_experimented_users(data, index):
     num_edits_of_groups = number_of_edits_by_user_category(data, index, 100, 0) 
# 1) we only want to know how many edits were done by the included users
     cond = (num_edits_of_groups['included'] == 1)
     edits_group_final = np.where(cond, num_edits_of_groups['nEditsgroup'], 0)
     num_edits_group_per_month = pd.DataFrame({'timestamp': num_edits_of_groups['timestamp'], 'n_edits': edits_group_final})
# 2) It is possible that the same month is repeated twice in the dataframe: 1. for the not included users (in which the n_edits column will always have a value of 0), 2. For the included users, in which the value of the n_edits column will be = number of edits done by the users in the category
     num_edits_group_per_month = num_edits_group_per_month.groupby(pd.Grouper(key='timestamp', freq='MS')).sum().reset_index()
     series = num_edits_group_per_month.set_index('timestamp')['n_edits'].rename_axis(None)
     if index is not None:
         series = series.reindex(index, fill_value=0)
     return series

#this metric gets the total number of editions per month that were done by new users (X = number of edits in all the history of the wiki -> x = 0 before the current month)
def number_of_edits_by_new_users(data, index):
     num_edits_of_groups = number_of_edits_by_user_category(data, index, 0, 0) 
# 1) we only want to know how many edits were done by the included users
     cond = (num_edits_of_groups['included'] == 1)
     edits_group_final = np.where(cond, num_edits_of_groups['nEditsgroup'], 0)
     num_edits_group_per_month = pd.DataFrame({'timestamp': num_edits_of_groups['timestamp'], 'n_edits': edits_group_final})
# 2) It is possible that the same month is repeated twice in the dataframe: 1. for the not included users (in which the n_edits column will always have a value of 0), 2. For the included users, in which the value of the n_edits column will be = number of edits done by the users in the category
     num_edits_group_per_month = num_edits_group_per_month.groupby(pd.Grouper(key='timestamp', freq='MS')).sum().reset_index()
     series = num_edits_group_per_month.set_index('timestamp')['n_edits'].rename_axis(None)
     if index is not None:
         series = series.reindex(index, fill_value=0)
     return series


def number_of_edits_by_category(data, index):
    nEdits_category1 = number_of_edits_by_beginner_users(data, index)
    nEdits_category2 = number_of_edits_by_advanced_users(data, index)
    nEdits_category3 = number_of_edits_by_experimented_users(data, index)
    nEdits_category4 = number_of_edits_by_highly_experimented_users(data, index)
    nEdits_category5 = number_of_edits_by_new_users(data, index)

    nEdits_category1.name = "n_edits_beginners"
    nEdits_category2.name = "n_edits_advanced"
    nEdits_category3.name = "n_edits_experimented"
    nEdits_category4.name = "n_edits_highly_experimented"
    nEdits_category5.name = "n_edits_new"

    return [nEdits_category1, nEdits_category2, nEdits_category3, nEdits_category4, nEdits_category5]


### 2) PERCENTAGE OF EDITIONS PER USER CATEGORY EACH MONTH ###

#this metric gets the percentage of editions per month that were done by beginner users (X = number of edits in all the history of the wiki -> x in [1,4])
def percentage_of_edits_by_beginner_users(data, index):
    return percentage_of_edits_by_user_category(data, index, 4, 1)

#this metric gets the percentage of editions per month that were done by advanced users (X = number of edits in all the history of the wiki -> x in [5,24])
def percentage_of_edits_by_advanced_users(data, index):
    return percentage_of_edits_by_user_category(data, index, 24, 5)

#this metric gets the percentage of editions per month that were done by experimented users (X = number of edits in all the history of the wiki -> x in [25,99])
def percentage_of_edits_by_experimented_users(data, index):
    return percentage_of_edits_by_user_category(data, index, 99, 25)

#this metric gets the percentage of editions per month that were done by highly experimented users (X = number of edits in all the history of the wiki -> x >= 100)
def percentage_of_edits_by_highly_experimented_users(data, index):
    return percentage_of_edits_by_user_category(data, index, 100, 0)

#this metric gets the percentage of editions per month that were done by new users (X = number of edits in all the history of the wiki -> x = 0 before the current month)
def percentage_of_edits_by_new_users(data, index):
    return percentage_of_edits_by_user_category(data, index, 0, 0)


def percentage_of_edits_by_category(data, index):
    pctage_category1 = percentage_of_edits_by_beginner_users(data, index)
    pctage_category2 = percentage_of_edits_by_advanced_users(data, index)
    pctage_category3 = percentage_of_edits_by_experimented_users(data, index)
    pctage_category4 = percentage_of_edits_by_highly_experimented_users(data, index)
    pctage_category5 = percentage_of_edits_by_new_users(data, index)

    pctage_category1.name = "pctage_beginners"
    pctage_category2.name = "pctage_advanced"
    pctage_category3.name = "pctage_experimented"
    pctage_category4.name = "pctage_highly_experimented"
    pctage_category5.name = "pctage_new"

    return [pctage_category1, pctage_category2, pctage_category3, pctage_category4, pctage_category5]


