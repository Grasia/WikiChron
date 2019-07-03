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
import datetime as d
from dateutil.relativedelta import relativedelta


def calculate_index_all_months(data):
    monthly_data = data.groupby(pd.Grouper(key='timestamp', freq='MS'))
    index = monthly_data.size().index
    return index



# Users


###### General helper functions ######

def set_category_name(list_of_series, list_of_names):
    '''
    Set the name to be given to each pd series.
    '''
    for i in range(len(list_of_series)):
        list_of_series[i].name = list_of_names[i]

def get_accum_number_of_edits_until_each_month(data, index):
    '''
    Returns a pd DataFrame with the suitable shape for calculating the metrics:
    one row contains the contributor_id, timestamp and nEdits -- cumulative number of edits done until the given timestamp
    '''
    df = data.groupby(['contributor_id']).apply(lambda x: x.groupby(pd.Grouper(key='timestamp', freq='MS')).size().to_frame('nEdits').reindex(index, fill_value=0).cumsum()).reset_index()
    return df

def get_monthly_number_of_edits(data, index):
    '''
    Adds a new column to the pd DataFrame given in data:
    one row contains the contributor_id, timestamp and monthly_nEdits -- monthly number of edits by the user
    '''
    cond = (data['contributor_id'] == data['contributor_id'].shift())
    data['monthly_nEdits'] = np.where(cond, data['nEdits'] - data['nEdits'].shift(), data['nEdits'])

def filter_df(data, condition, index):
    '''
    Filter the df in data, according to the given condition.
    Return a pd Series, with index = time index of the wiki, and data = number of users that fullfill the condition.
    '''
    users = data[condition]
    series = pd.Series(users.groupby(['timestamp']).size(), index).fillna(0)

    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series

def filter_anonymous(data):
    '''
    Erase anonymous users from the DataFrame in data
    '''
    data = data[data['contributor_name'] != 'Anonymous']
    return data

def calcultate_relative_proportion(list_of_category_series, list_of_column_names):
    '''
    Calculate the relative number of the data in each pd Series given in the list_of_category_series parameter.
    Return a pd DataFrame in which:
    -index = time index of the wiki.
    -A column per category with its relative proportion regarding the total in the month is computed.
    '''
    df = pd.concat(list_of_category_series, axis = 1)
    df['total'] = df[list_of_column_names].sum(axis=1)
    
    for i in range(len(list_of_column_names)):
        df[str(list_of_column_names[i])] = (df[str(list_of_column_names[i])]/df['total'])*100
    
    return df

def generate_list_of_dataframes(list_of_series, list_of_names):
    '''
    Return a list of pd DataFrames from the given list_of_series, using as column names the given list_of_names.
    '''
    list_of_dfs = []
    
    for i in range(len(list_of_names)):
        list_of_dfs.append(list_of_series[i].to_frame(str(list_of_names[i])))
    
    return list_of_dfs

#### Helper users active ####

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
    data = filter_anonymous(data)
    mothly = data.groupby(['contributor_id',pd.Grouper(key = 'timestamp', freq = 'MS')]).size().to_frame('size').reset_index()
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

def edition_concrete(data, index, pagType):
    filterData = data[data['page_ns'] == pagType]
    series = filterData.groupby([pd.Grouper(key ='timestamp', freq='MS')]).size()
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series
def rest_edition(data, index, listP):
    filterData = data
    for i in listP:
        filterData= filterData[filterData['page_ns'] != i]
    series = filterData.groupby([pd.Grouper(key ='timestamp', freq='MS')]).size()
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series

#### Helpers Users by Tenure ####

def add_position_column_users_first_edit(data):
    '''
    Add a new column to data:
    position: indicates the number of months since the the user's first contribution in the wiki
    '''
    cond = data['nEdits'] == 0
    data['position'] = np.where(cond, 0, data.groupby([cond, 'contributor_id']).cumcount() + 1)

def generate_condition_users_first_edit(data, x, y):
    '''
    Create a condition that the users must fulfill in order to be included in one of the categories of the users by tenure metric.
    '''
    if y > 0:
        condition = ((data['position'] >= x) & (data['position'] <= y)) & (data['nEdits'] != data['nEdits'].shift())
    elif (x == 1) and (y == 0):
        condition = ((data['position'] == x)) & (data['nEdits'] != data['nEdits'].shift())
    else:
        condition = (data['position'] > x) & (data['nEdits'] != data['nEdits'].shift())
    
    return condition

#### Helpers Users by the date of the last edit ####

def add_position_column_users_last_edit(data):
    '''
    Add a new column to data:
    position: indicates the number of months since the user's last contribution in the wikis
    '''
    cond = data['nEdits'] == 0
    data['position'] = np.where(cond, 0, data.groupby([cond, 'contributor_id', 'nEdits']).cumcount() + 1)
    
def generate_condition_users_last_edit(data, x):
    '''
    Create a condition that the users must fulfill in order to be included in one of the categories of the users by date of the last edit metric.
    '''
    if x != 6:
        condition = ((data['position'] == 1) & (data['position'].shift() == x)) & (data['contributor_id'] == data['contributor_id'].shift())
    else:
        condition = ((data['position'] == 1) & (data['position'].shift() > x)) & (data['contributor_id'] == data['contributor_id'].shift())

    return condition

#### Helper Active editors by Experience ####

def generate_condition_users_by_number_of_edits(data, x, y):
    '''
    Create a condition that the users must fulfill in order to be included in one of the categories of the Active editors by experience metric.
    '''
    if (y != 0) and (x > 0):
        condition = (data['contributor_id'].shift() == data['contributor_id']) & (data['nEdits'] != data['nEdits'].shift()) & ((data['nEdits'].shift()<=x) & (data['nEdits'].shift()>=y))
    elif (y == 0) and (x == 0):
        condition = (((data['nEdits'] > 0) & (data['nEdits'].shift() == 0)) & (data['contributor_id'] == data['contributor_id'].shift())) | ((data['contributor_id'] != data['contributor_id'].shift()) & (data['nEdits'] > 0))
    else:
        condition = (data['contributor_id'].shift() == data['contributor_id']) & (data['nEdits'] != data['nEdits'].shift()) & (data['nEdits'].shift()>=x)

    return condition

#### Helper metrics 9 and 10 ####

# this helper function gets the number of users that have edited a particular kind of page, specified by the parameter page_ns
def filter_users_pageNS(data, index, page_ns):
    data = filter_anonymous(data)
    edits_page = data[data['page_ns'] == page_ns]
    series = edits_page.groupby(pd.Grouper(key = 'timestamp', freq = 'MS'))['contributor_id'].nunique()
    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series


#### Helper metrics Edits by editor experience ####

def sum_monthly_edits_by_users(data, index):
    '''
    Return a pd Series with the sum of the monthly number of edits, stored in the monthly_nEdits column in the pd DataFrame given in data
    '''
    data = data.groupby(pd.Grouper(key='timestamp', freq='MS'))['monthly_nEdits'].sum().reset_index()
    series = data.set_index('timestamp')['monthly_nEdits'].rename_axis(None)

    if index is not None:
        series = series.reindex(index, fill_value=0)
    return series

###### Callable Functions ######

############################ New and Reincident users ###############################################################

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
    this_month.name = '1 month editing'
    two_three_months.name = 'btw. 2 and 3 consecutive months'
    four_six_months.name = 'btw. 4 and 6 consecutive months'
    more_six.name = 'more than 6 consecutive months'
    return [this_month, two_three_months, four_six_months, more_six]

def current_streak_only_mains(data, index):
    data = data[data['page_ns']==0]
    this_month = current_streak_this_month(data, index)
    two_three_months = current_streak_2_or_3_months_in_a_row(data, index)
    four_six_months = current_streak_4_or_6_months_in_a_row(data, index)
    more_six = current_streak_more_than_six_months_in_a_row(data, index)
    this_month.name = '1 month editing'
    two_three_months.name = 'btw. 2 and 3 consecutive months'
    four_six_months.name = 'btw. 4 and 6 consecutive months'
    more_six.name = 'more than 6 consecutive months'
    return [this_month, two_three_months, four_six_months, more_six]


def edition_on_type_pages(data, index):
    data=filter_anonymous(data)
    articles=edition_concrete(data, index, 0)
    talkPA=edition_concrete(data, index, 1)
    userP=edition_concrete(data, index, 2)
    talkPU=edition_concrete(data, index, 3)
    rest=rest_edition(data, index, [0,1,2,3])
    articles.name= 'Article pages'
    talkPA.name='Article talk pages'
    userP.name='User pages'
    talkPU.name='User talk pages'
    rest.name='Other pages'
    return [articles,talkPA,userP,talkPU,rest]

def edition_on_type_pages_extends_rest(data, index):
    data=filter_anonymous(data)
    #filt=rest_edition(data,index,[0,1,2,3])
    file=edition_concrete(data,index,6)
    mediaWiki=edition_concrete(data,index,8)
    template=edition_concrete(data,index,10)
    category=edition_concrete(data,index,14)
    rest=rest_edition(data,index,[0,1,2,3,6,8,10,14])
    file.name= 'File pages'
    mediaWiki.name='Media wiki pages'
    template.name='Template pages'
    category.name='Category pages'
    rest.name='Other pages'
    return [file,mediaWiki,template,category,rest]

############################ Users by tenure #################################################################################

def users_first_edit_between_1_3_months_ago(data, index):
    '''
    Get the users whose first edition was between 1 and 3 months ago
    '''
    condition = generate_condition_users_first_edit(data, 2, 4)
    return filter_df(data, condition, index)
    
def users_first_edit_between_4_6_months_ago(data, index):
    '''
    Get the users whose first edition was between 4 and 6 months ago
    '''
    condition = generate_condition_users_first_edit(data, 5, 7)
    return filter_df(data, condition, index)

def users_first_edit_between_6_12_months_ago(data, index):
    '''
    Get the users whose first edition was between 6 and 12 months ago
    '''
    condition = generate_condition_users_first_edit(data, 7, 13)
    return filter_df(data, condition, index)

def users_first_edit_more_than_12_months_ago(data, index):
    '''
    Get the users whose first edition was than 12 months ago
    '''
    condition = generate_condition_users_first_edit(data, 13, 0)
    return filter_df(data, condition, index)

def users_first_edit(data, index):
    '''Calculate the monthly number of users whose first edit was between 1 and 3, 4 and 6, 6 and 12, and more than 12 months ago
    '''
    data = filter_anonymous(data)
    format_data = get_accum_number_of_edits_until_each_month(data, index)
    add_position_column_users_first_edit(format_data)

    this_month = users_new(data, index)
    one_three = users_first_edit_between_1_3_months_ago(format_data, index)
    four_six = users_first_edit_between_4_6_months_ago(format_data, index)
    six_twelve = users_first_edit_between_6_12_months_ago(format_data, index)
    more_twelve = users_first_edit_more_than_12_months_ago(format_data, index)


    set_category_name([this_month, one_three, four_six, six_twelve, more_twelve], ['1st edit this month', '1st edit btw. 1 and 3 months ago', '1st edit btw. 4 and 6 months ago', '1st edit btw. 6 and 12 months ago', "1st edit more than 12 months ago"])
    
    return [this_month, one_three, four_six, six_twelve, more_twelve, 'Bar']

############################ Users by the date of the last edit ###########################################################################

def users_last_edit_1_month_ago(data, index):
    '''
    Get, among the users that have edited in that month X, the ones that have edited the last time in month X-1
    '''
    condition = generate_condition_users_last_edit(data, 1)
    return filter_df(data, condition, index)

def users_last_edit_2_or_3_months_ago(data, index):
    '''
    Get, among the users that have edited in month X, which ones have edited the last time in month X-2 or X-3
    '''
    condition = generate_condition_users_last_edit(data, 2)
    return filter_df(data, condition, index)

def users_last_edit_4_or_5_or_6_months_ago(data, index):
    '''
    Get, among the users that have edited in month X, the ones that have edited the last time in month X-4, X-5 or X-6
    '''
    condition = generate_condition_users_last_edit(data, 4)
    return filter_df(data, condition, index)

def users_last_edit_more_than_6_months_ago(data, index):
    '''
    Get, among the users that have edited in that month X, the ones that have edited the last time in any month > X-6
    '''
    condition = generate_condition_users_last_edit(data, 6)
    return filter_df(data, condition, index)

def users_last_edit(data, index):
    '''
    Get the monthly number of users whose last edit was less than 1, between 2 and 3, 4 and 6, and more than 6 months ago
    '''
    data = filter_anonymous(data)
    format_data = get_accum_number_of_edits_until_each_month(data, index)
    add_position_column_users_last_edit(format_data)

    this_month = users_new(data, index)
    one_month = users_last_edit_1_month_ago(format_data, index)
    two_three_months = users_last_edit_2_or_3_months_ago(format_data, index)
    four_six_months = users_last_edit_4_or_5_or_6_months_ago(format_data, index)
    more_six_months = users_last_edit_more_than_6_months_ago(format_data, index)

    set_category_name([this_month, one_month, two_three_months, four_six_months, more_six_months], ['new_users', 'last edit made 1 month ago', 'last edit made btw. 2 and 3 months ago', 'last edit made btw. 4 and 6 months ago', 'last edit made more than six months ago'])


    return [this_month, one_month, two_three_months, four_six_months, more_six_months, 'Bar']

############################ Active editors by experience #####################################################################

def users_number_of_edits_between_1_and_4(data, index):
    '''
    Get, among the users that make an edition in month X, which ones have done n editions, with n in [1,4], until month X-1
    '''
    condition = generate_condition_users_by_number_of_edits(data, 4, 1)
    return filter_df(data, condition, index)
 
def users_number_of_edits_between_5_and_24(data, index):
    '''
    Get, among the users that make an edition in month X, which ones have done n editions, with n in [5,24], until month X-1
    '''
    condition = generate_condition_users_by_number_of_edits(data, 24, 5)
    return filter_df(data, condition, index)

def users_number_of_edits_between_25_and_99(data, index):
    '''
    Get, among the users that make an edition in month X, which ones have done n editions, with n in [25,99], until month X-1
    '''
    condition = generate_condition_users_by_number_of_edits(data, 99, 25)
    return filter_df(data, condition, index)

def users_number_of_edits_highEq_100(data, index):
    '''
    Get, among the users that make an edition in month X, which ones have done n editions, with n>=100, until month X-1
    '''
    condition = generate_condition_users_by_number_of_edits(data, 100, 0)
    return filter_df(data, condition, index)

def users_number_of_edits(data, index):
    '''
    Get the monthly number of users that belong to each category, in the Active editors by experience metric.
    '''
    data = filter_anonymous(data)
    format_data = get_accum_number_of_edits_until_each_month(data, index)
    
    new_users = users_new(data, index)
    one_four = users_number_of_edits_between_1_and_4(format_data, index)
    between_5_24 = users_number_of_edits_between_5_and_24(format_data, index)
    between_25_99 = users_number_of_edits_between_25_and_99(format_data, index)
    highEq_100 = users_number_of_edits_highEq_100(format_data, index)

    set_category_name([new_users, one_four, between_5_24, between_25_99, highEq_100], ['New users', 'Btw. 1 and 4 edits', 'Btw. 5 and 24 edits', 'Btw. 25 and 99 edits', 'More than 99 edits'])


    return [new_users, one_four, between_5_24, between_25_99, highEq_100, 'Bar']

def users_number_of_edits_abs(data, index):

    '''
    Get the absolute proportion of users that belong to each category, in the Active editors by experience metric.
    '''
    users_num_edits = users_number_of_edits(data, index)

    list_of_category_names = ['new_users', 'one_four', '5_24', '25_99', 'highEq_100']
    list_of_categories = generate_list_of_dataframes(users_num_edits, list_of_category_names)
    df = calcultate_relative_proportion(list_of_categories, list_of_category_names)

    new_users = pd.Series(df['new_users'], index = index)
    one_four = pd.Series(df['one_four'], index = index)
    between_5_24 = pd.Series(df['5_24'], index = index)
    between_25_99 = pd.Series(df['25_99'], index = index)
    highEq_100 = pd.Series(df['highEq_100'], index = index)

    set_category_name([new_users, one_four, between_5_24, between_25_99, highEq_100], ['New users', 'Btw. 1 and 4 edits', 'Btw. 5 and 24 edits', 'Btw. 25 and 99 edits', 'More than 99 edits'])
 
    return [new_users, one_four, between_5_24, between_25_99, highEq_100, 'Bar']

############################ Active editors by namespace #####################################################################################

def users_article_page(data, index):
    '''
    Monthly number of users that have edited a main page
    '''
    return filter_users_pageNS(data, index, 0)

def users_articletalk_page(data, index):
    '''
    Monthly number of users that have edited an article talk page
    '''
    return filter_users_pageNS(data, index, 1)

def users_user_page(data, index):
    '''
    Monthly number of users that have edited a user page
    '''
    return filter_users_pageNS(data, index, 2)

def users_template_page(data, index):
    '''
    Monthly number of users that have edited a template page
    '''
    return filter_users_pageNS(data, index, 10)

def users_usertalk_page(data,index):
    '''
    Monthly number of users that have edited a talk page
    '''
    return filter_users_pageNS(data, index, 3)

def users_other_page(data,index):
    '''
    Monthly number of users that have edited the rest of relevant namespaces in the wiki
    '''
    category_list = [-2, -1, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 110, 111]

    aux = pd.DataFrame()
    aux['timestamp'] = index

    for i in range(len(category_list)):
        serie = filter_users_pageNS(data, index, category_list[i])
        serie = pd.DataFrame(serie).reset_index()
        aux['page_ns_' + str(category_list[i])] = serie['contributor_id']

    aux['final_result'] = aux.sum(axis=1)
    series = pd.Series(index=aux['timestamp'], data=aux['final_result'].values)
    return series

def users_in_namespaces(data, index):
    '''
    Get the monthly number of users that belong to each category in the Active editors in namespaces metric
    '''
    data = filter_anonymous(data)

    main_page = users_article_page(data, index)
    articletalk_page = users_articletalk_page(data, index)
    user_page = users_user_page(data, index)
    template_page = users_template_page(data, index)
    usertalk_page = users_usertalk_page(data,index)
    other_page = users_other_page(data,index)

    set_category_name([main_page, articletalk_page, user_page, template_page, usertalk_page, other_page], ['Article pages', 'Article talk pages', 'User pages', 'Template pages', 'User talk pages', 'Other pages'])

    return [other_page, main_page, articletalk_page, user_page, template_page, usertalk_page]

############################ Edits by editor experience (absolute and relative) #########################################

def number_of_edits_by_beginner_users(data, index):

    '''
    Get the total number of editions per month that were done by users who have made between 1 and 4 editions in all the history of the wiki
    '''
    condition = generate_condition_users_by_number_of_edits(data, 4, 1)
    users = data[condition]

    return sum_monthly_edits_by_users(users, index)


def number_of_edits_by_advanced_users(data, index):

    '''
    Get the total number of editions per month that were done by users who have made between 5 and 24 editions in all the history of the wiki
    '''
    condition = generate_condition_users_by_number_of_edits(data, 24, 5)
    users = data[condition]

    return sum_monthly_edits_by_users(users, index)

def number_of_edits_by_experimented_users(data, index):

    '''
    Get the total number of editions per month that were done by users who have made between 25 and 99 editions in all the history of the wiki
    '''
    condition = generate_condition_users_by_number_of_edits(data, 99, 25)
    users = data[condition]

    return sum_monthly_edits_by_users(users, index)

def number_of_edits_by_highly_experimented_users(data, index):

    '''
    Get the total number of editions per experience (absolute and relative)month that were done by users who have made more than 100 editions in all the history of the wiki
    '''
    condition = generate_condition_users_by_number_of_edits(data, 100, 0)
    users = data[condition]

    return sum_monthly_edits_by_users(users, index)


def number_of_edits_by_new_users_experience(data, index):
    '''
    Get the total number of editions per month that were done by new users
    '''
    condition = generate_condition_users_by_number_of_edits(data, 0, 0)
    users = data[condition]

    return sum_monthly_edits_by_users(users, index)

def number_of_edits_by_experience(data, index):
    '''
    Get the monthly number of edits by each user category in the Active editors by experience metric
    '''
    data = filter_anonymous(data)
    data = get_accum_number_of_edits_until_each_month(data, index)
    get_monthly_number_of_edits(data, index)

    nEdits_category1 = number_of_edits_by_beginner_users(data, index)
    nEdits_category2 = number_of_edits_by_advanced_users(data, index)
    nEdits_category3 = number_of_edits_by_experimented_users(data, index)
    nEdits_category4 = number_of_edits_by_highly_experimented_users(data, index)
    nEdits_category5 = number_of_edits_by_new_users_experience(data, index)

    set_category_name([nEdits_category1, nEdits_category2, nEdits_category3, nEdits_category4, nEdits_category5], ["Edits by beginners (btw. 1 and 4 edits)", "Edits by advanced (btw. 5 and 24 edits)", "Edits by experimented (btw. 24 and 99 edits)", "Edits by highly experimented (more than 99 edits)", "Edits by new users"])

    return [nEdits_category5, nEdits_category1, nEdits_category2, nEdits_category3, nEdits_category4]

def number_of_edits_by_experience_abs(data, index):
    '''
    Get the monthly proportion of edits done by each user category in the Active editors by experience metrics
    '''
    edits_by_category = number_of_edits_by_experience(data, index)
    list_of_category_names = ["% of edits by new users", "% of edits by beginners (btw. 1 and 4 edits)", "% of edits by advanced (btw. 5 and 24 edits)", "% of edits by experimented (btw. 24 and 99 edits)", "% of edits by highly experimented (more than 99 edits)"]
    list_of_edits_by_category = generate_list_of_dataframes(edits_by_category, list_of_category_names)
    df = calcultate_relative_proportion(list_of_edits_by_category, list_of_category_names)

    edits_new_users = pd.Series(df[list_of_category_names[0]], index = index)
    edits_beginners = pd.Series(df[list_of_category_names[1]], index = index)
    edits_advanced = pd.Series(df[list_of_category_names[2]], index = index)
    edits_experimented = pd.Series(df[list_of_category_names[3]], index = index)
    edits_H_experimented = pd.Series(df[list_of_category_names[4]], index = index)

    set_category_name([edits_new_users, edits_beginners, edits_advanced, edits_experimented, edits_H_experimented], list_of_category_names)

    return [edits_new_users, edits_beginners, edits_advanced, edits_experimented, edits_H_experimented, 'Bar']


############################ Edits by editor's tenure #########################################

def number_of_edits_by_new_users_tenure(data, index):
    '''
    Get the total number of edits done by users whose first edit was this month
    '''
    condition = generate_condition_users_first_edit(data, 1, 0)
    users = data[condition]
    return sum_monthly_edits_by_users(users, index)

def number_of_edits_by_users_first_edit_between_1_3_months_ago(data, index):
    '''
    Get the total number of edits done by users whose first edit was between 1 and 3 months ago
    '''
    condition = generate_condition_users_first_edit(data, 2, 4)
    users = data[condition]
    return sum_monthly_edits_by_users(users, index)

def number_of_edits_by_users_first_edit_between_4_6_months_ago(data, index):
    '''
    Get the total number of edits done by users whose first edit was between 4 and 6 months ago
    '''
    condition = generate_condition_users_first_edit(data, 5, 7)
    users = data[condition]
    return sum_monthly_edits_by_users(users, index)

def number_of_edits_by_users_first_edit_between_6_12_months_ago(data, index):
    '''
    Get the total number of edits done by users whose first edit was between 6 and 12 months ago
    '''
    condition = generate_condition_users_first_edit(data, 7, 13)
    users = data[condition]
    return sum_monthly_edits_by_users(users, index)

def number_of_edits_by_users_first_edit_more_12_months_ago(data, index):
    '''
    Get the total number of edits done by users whose first edit was more than 12 months ago
    '''
    condition = generate_condition_users_first_edit(data, 13, 0)
    users = data[condition]
    return sum_monthly_edits_by_users(users, index)

def number_of_edits_by_tenure(data, index):
    '''
    Get the monthly number of edits by each user category in the Users by tenure metric
    '''
    #data = filter_anonymous(data)
    data = get_accum_number_of_edits_until_each_month(data, index)
    add_position_column_users_first_edit(data)
    get_monthly_number_of_edits(data, index)

    nEdits_category1 = number_of_edits_by_new_users_tenure(data, index)
    nEdits_category2 = number_of_edits_by_users_first_edit_between_1_3_months_ago(data, index)
    nEdits_category3 = number_of_edits_by_users_first_edit_between_4_6_months_ago(data, index)
    nEdits_category4 = number_of_edits_by_users_first_edit_between_6_12_months_ago(data, index)
    nEdits_category5 = number_of_edits_by_users_first_edit_more_12_months_ago(data, index)

    set_category_name([nEdits_category1, nEdits_category2, nEdits_category3, nEdits_category4], ["Edits by new users", "Edits by users whose 1st edit was btw. 1 and 3 months ago", "Edits by users whose 1st edit was btw. 4 and 6 months ago", "Edits by users whose 1st edit was btw. 6 and 12 months ago", "Edits by users whose 1st edit was more than 12 months ago"])

    return [nEdits_category1, nEdits_category2, nEdits_category3, nEdits_category4, nEdits_category5, 'Bar']

def number_of_edits_by_tenure_abs(data, index):
    '''
    Get the monthly proportion of edits done by each user category in the Users by tenure metric
    '''
    edits_by_category = number_of_edits_by_tenure(data, index)
    list_of_category_names = ["% of edits by new users", "% of edits by users whose 1st edit was btw. 1 and 3 months ago", "% of edits by users whose 1st edit was btw. 4 and 6 months ago", "% of edits by users whose 1st edit was btw. 6 and 12 months ago", "% of edits by users whose 1st edit was more than 12 months ago"]
    list_of_edits_by_category = generate_list_of_dataframes(edits_by_category, list_of_category_names)
    df = calcultate_relative_proportion(list_of_edits_by_category, list_of_category_names)

    edits_new_users = pd.Series(df[list_of_category_names[0]], index = index)
    edits_1_3 = pd.Series(df[list_of_category_names[1]], index = index)
    edits_4_6 = pd.Series(df[list_of_category_names[2]], index = index)
    edits_6_12 = pd.Series(df[list_of_category_names[3]], index = index)
    edits_12 = pd.Series(df[list_of_category_names[4]], index = index)

    set_category_name([edits_new_users, edits_1_3, edits_4_6, edits_6_12, edits_12], list_of_category_names)

    return [edits_new_users, edits_1_3, edits_4_6, edits_6_12, edits_12, 'Bar']
>>>>>>> ffb35a9... added new edit distribution metrics: edits by editor's tenure (relative and absolute)

############################# Returning and surviving new editors ############################################

def returning_new_editor(data, index):
    data.reset_index(drop=True, inplace=True)
    #remove anonymous users
    registered_users = filter_anonymous(data)
    #add up 7 days to the date on which each user registered
    seven_days_after_registration = registered_users.groupby(['contributor_id']).agg({'timestamp':'first'}).apply(lambda x: x+d.timedelta(days=7)).reset_index()
    #change the name to the timestamp column
    seven_days_after_registration=seven_days_after_registration.rename(columns = {'timestamp':'seven_days_after'})
    #merge two dataframes by contributor_id
    registered_users = pd.merge(registered_users, seven_days_after_registration, on ='contributor_id')
    #edits of each user within 7 days of being registered
    registered_users = registered_users[registered_users['timestamp'] <=registered_users['seven_days_after']]
    #to order by date
    registered_users = registered_users.sort_values(['timestamp'])
    #get the timestamp and contributor_id and group by contributor_id
    timestamp_and_contributor_id = registered_users[['timestamp', 'contributor_id']].groupby(['contributor_id'])
    #displace the timestamp a position 
    displace_timestamp = timestamp_and_contributor_id.apply(lambda x: x.shift())
    registered_users['displace_timestamp'] = displace_timestamp['timestamp']
    #compare the origin timestamp with the displace_timestamp
    registered_users['comp'] = (registered_users.timestamp-registered_users.displace_timestamp)
    #convert to seconds and replace the NAT for 31 because the NAT indicate the first edition
    registered_users['comp'] = registered_users['comp'].apply(lambda y: y.total_seconds()/60).fillna(61)
    #take the edit sessions
    edits_sessions = registered_users[(registered_users['comp']>60) ]
    num_edits_sessions = edits_sessions.groupby([pd.Grouper(key='timestamp', freq='MS'), 'contributor_id']).size()
    #users with at least two editions
    returning_users = num_edits_sessions[num_edits_sessions >1].to_frame('returning_users').reset_index()
    #minimum month in which each user has made two editions
    returning_new_users = returning_users.groupby(['contributor_id'])['timestamp'].min().reset_index()
    returning_new_users = returning_new_users.groupby(pd.Grouper(key='timestamp', freq='MS')).size()
    if index is not None:
        returning_new_users = returning_new_users.reindex(index, fill_value=0)
    return [returning_new_users, 'Scatter']
	
def surviving_new_editor(data, index):
    data.reset_index(drop=True, inplace=True)
    registered_users = filter_anonymous(data)
    #add up 30 days to the date on which each user registered
    thirty_days_after_registration = registered_users.groupby(['contributor_id']).agg({'timestamp':'first'}).apply(lambda x: x+d.timedelta(days=30)).reset_index()
    thirty_days_after_registration=thirty_days_after_registration.rename(columns = {'timestamp':'thirty_days_after'})
    registered_users = pd.merge(registered_users, thirty_days_after_registration, on ='contributor_id')
    registered_users['survival period'] = registered_users['thirty_days_after'].apply(lambda x: x+d.timedelta(days=30))
    survival_users = registered_users[(registered_users['timestamp'] >= registered_users['thirty_days_after']) & (registered_users['timestamp'] <= registered_users['survival period'])]
    survival_users = survival_users.groupby([pd.Grouper(key='timestamp', freq='MS'), 'contributor_id']).size().to_frame('num_editions_in_survival_period').reset_index()
    survival_new_users = survival_users.groupby(['contributor_id'])['timestamp'].max().reset_index()
    survival_new_users = survival_new_users.groupby(pd.Grouper(key='timestamp', freq='MS')).size()
    if index is not None:
        survival_new_users = survival_new_users.reindex(index, fill_value=0)
    return [survival_new_users, 'Scatter']

############################# HEATMAP METRICS ##############################################

def edit_distributions_across_editors(data, index):
    """
    Function which calculates the number X of editors making the same number of editions.
    it returns the months of the wiki, a list of the number of contributions until the maximum number,
    and at last, a matrix with the number of contributors doing the same number of contributions on each month.

    """
    users_registered = filter_anonymous(data)
    mothly = users_registered.groupby([pd.Grouper(key ='timestamp', freq='MS'),'contributor_id']).size()
    max_contributions = max(mothly)
    mothly = mothly.to_frame('num_contributions').reset_index()
    mothly = mothly.groupby([pd.Grouper(key ='timestamp', freq='MS'),'num_contributions']).size().to_frame('num_editors').reset_index()
    max_persons = max(mothly['num_editors'])
    round_max = round((max_contributions+5), -1)
    list_range = list(range(0, round_max+1, 10))
    max_range = max(list_range)
    mothly['range'] = pd.cut(mothly['num_contributions'], bins = list_range).astype(str)
    months_range = mothly.groupby([pd.Grouper(key ='timestamp', freq='MS'), 'range']).size()
    graphs_list = [[0 for j in range(max_range+1)] for i in range(len(index))]
    before = pd.to_datetime(0)
    j = -1
    for i, v in months_range.iteritems():
        i = list(i)
        current = i[0]
        p = i[1]
        p = p.split(']')[0]
        p = p.split('(')[1]
        p = p.split(',')
        num_min = int(float(p[0]))
        num_max = int(float(p[1]))
        num_min = (num_min+1)
        num_max = (num_max)
        resta = current - before
        resta = int(resta / np.timedelta64(1, 'D'))
        while (resta > 31 and before != pd.to_datetime(0)):
            j = j+1
            resta = resta-31
        if (before != current):
            j = j +1
            before = current
        for num in range(num_min,num_max+1):
            graphs_list[j][num] = v


    wiki_by_metrics = []
    for metric_idx in range(max_contributions+1):
        metric_row = [graphs_list[wiki_idx].pop(0) for wiki_idx in range(len(graphs_list))]
        wiki_by_metrics.append(metric_row) 
    return [index,list(range(max_contributions)), wiki_by_metrics, months_range]

def bytes_difference_across_articles(data, index):
    data.set_index(data['timestamp'], inplace=True)
    users_registered = filter_anonymous(data)
    mains = users_registered[users_registered['page_ns'] == 0]
    order = mains.sort_index()
    group_by_page_id = order[['page_id', 'bytes']].groupby(['page_id'])
    frame_bytes = group_by_page_id.apply(lambda x: (x.bytes-x.bytes.shift()).fillna(x.bytes)).to_frame('dif')
    #frame_bytes['dif'] = group_by_page_id.apply(lambda x: x.bytes-x.bytes.shift())
    #frame_bytes['dif'] = frame_bytes['dif'].fillna(frame_bytes['bytes'])
    frame_bytes['dif'] = frame_bytes['dif'].apply(lambda x: int(x))
    frame_bytes = frame_bytes.reset_index()
    max_dif_bytes = int(max(frame_bytes['dif']))
    min_dif_bytes = int(min(frame_bytes['dif'])-1)
    round_max = (max_dif_bytes+100)
    list_range = list(range(min_dif_bytes, round_max, 100))
    max_range = max(list_range)
    frame_bytes['range'] = pd.cut(frame_bytes['dif'], bins = list_range).astype(str)
    months_range = frame_bytes.groupby([pd.Grouper(key ='timestamp', freq='MS'), 'range']).size()
    min_dif_bytes_a = abs(min_dif_bytes+1)
    max_range = max_range + min_dif_bytes_a
    graphs_list = [[0 for j in range(max_range)] for i in range(len(index))]
    before = pd.to_datetime(0)
    j = -1
    for i, v in months_range.iteritems():
        i = list(i)
        current = i[0]
        p = i[1]
        p = p.split(']')[0]
        p = p.split('(')[1]
        p = p.split(',')
        num_min = int(float(p[0]))
        num_max = int(float(p[1]))
        num_min = (num_min+1)
        num_max = (num_max)
        resta = current - before
        resta = int(resta / np.timedelta64(1, 'D'))
        while (resta > 31 and before != pd.to_datetime(0)):
            j = j+1
            resta = resta-31
        if (before != current):
            j = j +1
            before = current
        for num in range(num_min,num_max):
            graphs_list[j][num] = v

    wiki_by_metrics = []
    for metric_idx in range(max_dif_bytes+1):
        metric_row = [graphs_list[wiki_idx].pop(0) for wiki_idx in range(len(graphs_list))]
        wiki_by_metrics.append(metric_row) 
    return [index, list(range(min_dif_bytes, max_dif_bytes)), wiki_by_metrics, months_range]

def edition_on_pages(data, index):
    users_registered = filter_anonymous(data)
    groupTP=users_registered.groupby([pd.Grouper(key ='timestamp', freq='MS'),'page_id']).size().to_frame('ediciones').reset_index()
    maxEditors=max(groupTP['ediciones'])
    round_max = (maxEditors+5)
    list_range = list(range(0, round_max+1, 5))
    max_range = max(list_range)
    groupTP['range'] = pd.cut(groupTP['ediciones'], bins = list_range).astype(str)
    z = groupTP.groupby([pd.Grouper(key ='timestamp', freq='MS'), 'range']).size()
    graphs_list = [[0 for j in range(max_range+1)] for i in range(len(index))]
    before = pd.to_datetime(0)
    j = -1
    for i, v in z.iteritems():
        i = list(i)
        current = i[0]
        p = i[1]
        p = p.split(']')[0]
        p = p.split('(')[1]
        p = p.split(',')
        num_min = int(float(p[0]))
        num_max = int(float(p[1]))
        num_min = (num_min+1)
        num_max = (num_max)
        resta = current - before
        resta = int(resta / np.timedelta64(1, 'D'))
        while (resta > 31 and before != pd.to_datetime(0)):
            j = j+1
            resta = resta-31
        if (before != current):
            j = j +1
            before = current
        for num in range(num_min,num_max+1):
            graphs_list[j][num] = v
    wiki_by_metrics = []
    for metric_idx in range(maxEditors+1):
            metric_row = [graphs_list[wiki_idx].pop(0) for wiki_idx in range(len(graphs_list))]
            wiki_by_metrics.append(metric_row) 
    return [index,list(range(maxEditors)),wiki_by_metrics, z]

def revision_on_pages(data, index):
    users_registered = filter_anonymous(data)
    without_first_edition = users_registered.groupby([pd.Grouper(key ='timestamp', freq='MS'),'page_id']).apply(lambda x:x.iloc[1:,1:])
    z=without_first_edition.groupby([pd.Grouper(key ='timestamp', freq='MS'),'page_id']).size().to_frame('revisiones').reset_index()
    maxRevision= max(z['revisiones'])
    round_max = (maxRevision+5)
    list_range = list(range(0, round_max+1, 5))
    max_range = max(list_range)
    z['range'] = pd.cut(z['revisiones'], bins = list_range).astype(str)
    z = z.groupby([pd.Grouper(key ='timestamp', freq='MS'), 'range']).size()
    graphs_list = [[0 for j in range(max_range+1)] for i in range(len(index))]
    before = pd.to_datetime(0)
    j = -1
    for i, v in z.iteritems():
        i = list(i)
        current = i[0]
        p = i[1]
        p = p.split(']')[0]
        p = p.split('(')[1]
        p = p.split(',')
        num_min = int(float(p[0]))
        num_max = int(float(p[1]))
        num_min = (num_min+1)
        num_max = (num_max)
        resta = current - before
        resta = int(resta / np.timedelta64(1, 'D'))
        while (resta > 31 and before != pd.to_datetime(0)):
            j = j+1
            resta = resta-31
        if (before != current):
            j = j +1
            before = current
        for num in range(num_min,num_max+1):
            graphs_list[j][num] = v
    wiki_by_metrics = []
    for metric_idx in range(maxRevision+1):
            metric_row = [graphs_list[wiki_idx].pop(0) for wiki_idx in range(len(graphs_list))]
            wiki_by_metrics.append(metric_row)
    return [index,list(range(maxRevision)),wiki_by_metrics, z]

def distribution_editors_between_articles_edited_each_month(data, index):
    users_registered = filter_anonymous(data)
    #main namespace
    users_registered = users_registered[users_registered['page_ns']==0]

    users_per_article = users_registered.groupby([pd.Grouper(key ='timestamp', freq='MS'),'page_id'])['contributor_id'].nunique().reset_index(name='editor_count')

    max_editors = max(users_per_article['editor_count'])

    z_articles_by_y_editors = users_per_article.groupby([pd.Grouper(key ='timestamp', freq='MS'),'editor_count']).size()


    #y parameter
    y_param = list(range(max_editors))

    #z parameter
    graphs_list = [[0 for j in range(max_editors+1)] for i in range(len(index))]
    anterior = pd.to_datetime(0)
    j = -1
    for i, v in z_articles_by_y_editors.iteritems():
        i = list(i)
        actual = i[0]
        num = i[1]
        resta = actual - anterior
        resta = int(resta / np.timedelta64(1, 'D'))
        while (resta > 31 and anterior != pd.to_datetime(0)):
            j = j+1
            resta = resta-31
        if (anterior != actual):
            j = j +1
            anterior = actual
        if(j <= len(index)):
            graphs_list[j][num] = v

    z_param = []
    for i in range(max_editors+1):
            row = [graphs_list[j].pop(0) for j in range(len(graphs_list))]
            z_param.append(row)  
    return [index,y_param,z_param, z_articles_by_y_editors]

def changes_in_absolute_size_of_editor_classes(data, index):
    class1 = users_number_of_edits_between_1_and_4(data, index).to_frame('one_four')
    class2 = users_number_of_edits_between_5_and_24(data, index).to_frame('5_24')
    class3 = users_number_of_edits_between_25_and_99(data, index).to_frame('25_99')
    class4 = users_number_of_edits_highEq_100(data, index).to_frame('highEq_100')
    concatenate = pd.concat([class1, class2, class3, class4], axis = 1)
    concatenate['suma'] = concatenate[['one_four', '5_24', '25_99', 'highEq_100']].sum(axis=1)
    concatenate = concatenate.transpose()
    # With this data, we can start calculating the heatmap axises:
    months = data.groupby(pd.Grouper(key ='timestamp', freq='MS'))
    months = months.size()
    classes = ['between 1 and 4 edits', 'between 5 and 24 edits', 'between 25 and 99 edits', '>= 100 edits' ]
    graphs_list = [[0 for j in range(len(index))] for i in range(len(classes))]

    for i in range(len(classes)):

        for j in range(len(index)):

            if (j == 0):
                graphs_list[i][j] = concatenate.iloc[i, j]

            else:

                if (concatenate.iloc[i, j] == concatenate.iloc[i, j - 1]):
                        graphs_list[i][j] = 0

                elif (concatenate.iloc[i, j] < concatenate.iloc[i, j - 1]):
                    graphs_list[i][j] = -(concatenate.iloc[i, j - 1] - concatenate.iloc[i, j])

                elif (concatenate.iloc[i, j] > concatenate.iloc[i, j - 1]):
                        graphs_list[i][j] = concatenate.iloc[i, j] - concatenate.iloc[i, j - 1]
    return[months.index, classes, graphs_list, concatenate]

########################### % Of edits by % of users (accumulated and monthly) ###########################################

def contributor_pctg_per_contributions_pctg(data, index):
    """
    Function which calculates which % of contributors has contributed
    in a 50%, 80%, 90% and 99% of the total wiki edits until each month.
    """
    data = filter_anonymous(data)
    new_index = data.groupby(pd.Grouper(key='timestamp', freq='MS')).size().to_frame('months').index

    users_month_edits = data.groupby(['contributor_id']).apply(lambda x: x.groupby(pd.Grouper(key='timestamp', freq='MS')).size().to_frame('nEdits_cumulative').reindex(new_index, fill_value=0).cumsum()).reset_index()

# 2) Add a new column which contains the total number of edits on each month (this value is cumulative aswell)
    users_month_edits = users_month_edits.groupby([pd.Grouper(key='timestamp', freq='MS'),'contributor_id']).sum().reset_index()
    users_month_edits['nEdits_month'] = users_month_edits.groupby(pd.Grouper(key='timestamp', freq='MS'))['nEdits_cumulative'].transform('sum')

# 3) Now, we want to calculate the percentage of edits that each user has done on each month: add a new column, 'edits_pctg'
    users_month_edits['edits%'] = (users_month_edits['nEdits_cumulative']/users_month_edits['nEdits_month'])*100

# 4) Order the dataframe in ascending order according to the column 'edit_pctg' and according to the timestamp, as we want to keep the order inside each group:
    users_month_edits = users_month_edits.sort_values(['timestamp', 'edits%'], ascending=[True, False])

# 5) calculate the cumulative percentage per month, in a new column: 'edit_cumulative_pctg'
    users_month_edits['edits%_accum'] = users_month_edits.groupby(pd.Grouper(key='timestamp', freq='MS'))['edits%'].cumsum()

# 6) traverse the dataframe: we want to calculate the %X of contributors that does a %Y of contributions (being Y = 50%, 80%, 90% and 99%) PER MONTH.
# 6.1) Note: final is the final dataframe, of shape: timestamp, category50, category80, category90, category99. These columns contain the %X of contributors that have contributed each month to create 50, 80, 90 and 99% of editions

    users_month_edits = users_month_edits.set_index('timestamp')
    lst_dict = []
    cols = ['timestamp', 'category50%', 'category80%', 'category90%', 'category99%', 'category_upper']

    for idx in users_month_edits.index.unique():
        group = users_month_edits.loc[idx]
        #on each month, for the total contributors we don't count the contributors whose collaboration is 0%.
        group = group[group['edits%'] > 0]
        num_contributors = group.shape[0]
        category50 = group[(group['edits%_accum'] <= 50) & (group['edits%_accum'] > 0)].shape[0]
        category80 = group[(group['edits%_accum'] <= 80) & (group['edits%_accum'] > 50)].shape[0]
        category90 = group[(group['edits%_accum'] <= 90) & (group['edits%_accum'] > 80)].shape[0]
        category99 = group[(group['edits%_accum'] <= 99) & (group['edits%_accum'] > 90)].shape[0]
        cat_upper = group[group['edits%_accum'] > 99].shape[0]
        daux = {'timestamp':idx, 'category50%':(category50/num_contributors)*100, 'category80%':(category80/num_contributors) * 100, 'category90%':(category90/num_contributors) * 100,'category99%':(category99/num_contributors) * 100, 'category_upper':(cat_upper/num_contributors) * 100}
        lst_dict.append(daux)

    final_df = pd.DataFrame(columns = cols, data = lst_dict)
    category_50 = pd.Series(index=final_df['timestamp'], data=final_df['category50%'].values)
    category_80 = pd.Series(index=final_df['timestamp'], data=final_df['category80%'].values)
    category_90 = pd.Series(index=final_df['timestamp'], data=final_df['category90%'].values)
    category_99 = pd.Series(index=final_df['timestamp'], data=final_df['category99%'].values)
    category_upper = pd.Series(index=final_df['timestamp'], data=final_df['category_upper'].values)
    category_50.name = "50% of edits"
    category_80.name = "80% of edits"
    category_90.name = "90% of edits"
    category_99.name = "99% of edits"
    category_upper.name = "100% of edits"

    return[category_50, category_80, category_90, category_99, category_upper]

def contributor_pctg_per_contributions_pctg_per_month(data, index):
    data = filter_anonymous(data)
    new_index = data.groupby(pd.Grouper(key='timestamp', freq='MS')).size().to_frame('months').index

    users_month_edits =data.groupby(['contributor_id']).apply(lambda x: x.groupby(pd.Grouper(key='timestamp', freq='MS')).size().to_frame('nEdits_cumulative').reindex(new_index, fill_value=0).cumsum()).reset_index()

    # 2.1) Get the non accum value of edits
    cond = (users_month_edits['contributor_id'] == users_month_edits['contributor_id'].shift())
    users_month_edits['nEdits_non_accum'] = np.where(cond, users_month_edits['nEdits_cumulative'] - users_month_edits['nEdits_cumulative'].shift(), users_month_edits['nEdits_cumulative'])

    # 2) Add a new column which contains the total number of edits on each month (this value is NOT accumulated)
    users_month_edits = users_month_edits.groupby([pd.Grouper(key='timestamp', freq='MS'),'contributor_id']).sum().reset_index()
    users_month_edits['nEdits_month'] = users_month_edits.groupby(pd.Grouper(key='timestamp', freq='MS'))['nEdits_non_accum'].transform('sum')

    # 3) Now, we want to calculate the percentage of edits that each user has done on each month: add a new column, 'edits_pctg'
    users_month_edits['edits%'] = (users_month_edits['nEdits_non_accum']/users_month_edits['nEdits_month'])*100

    # 4) Order the dataframe in ascending order according to the column 'edit_pctg' and according to the timestamp, as we want to keep the order inside each group:
    users_month_edits = users_month_edits.sort_values(['timestamp', 'edits%'], ascending=[True, False])

    # 5) calculate the cumulative percentage per month, in a new column: 'edit_cumulative_pctg'
    users_month_edits['edits%_accum'] = users_month_edits.groupby(pd.Grouper(key='timestamp', freq='MS'))['edits%'].cumsum()

    # 6) traverse the dataframe: we want to calculate the %X of contributors that does a %Y of contributions (being Y = 50%, 80%, 90% and 99%) PER MONTH.
    # 6.1) Note: final is the final dataframe, of shape: timestamp, category50, category80, category90, category99. These columns contain the %X of contributors that have contributed each month to create 50, 80, 90 and 99% of editions
    users_month_edits = users_month_edits.set_index('timestamp')
    lst_dict = []
    cols = ['timestamp', 'category50%', 'category80%', 'category90%', 'category99%', 'category_upper']
    for idx in users_month_edits.index.unique():
        group = users_month_edits.loc[idx]
        #on each month, for the total contributors we don't count the contributors whose collaboration is 0%.
        group = group[group['edits%'] > 0]
        num_contributors = group.shape[0]
        if (num_contributors > 0):
            category50 = group[(group['edits%_accum'] <= 50) & (group['edits%_accum'] > 0)].shape[0]
            category80 = group[(group['edits%_accum'] <= 80) & (group['edits%_accum'] > 50)].shape[0]
            category90 = group[(group['edits%_accum'] <= 90) & (group['edits%_accum'] > 80)].shape[0]
            category99 = group[(group['edits%_accum'] <= 99) & (group['edits%_accum'] > 90)].shape[0]
            cat_upper = group[group['edits%_accum'] > 99].shape[0]
            daux = {'timestamp':idx, 'category50%':(category50/num_contributors)*100, 'category80%':(category80/num_contributors) * 100, 'category90%':(category90/num_contributors) * 100,'category99%':(category99/num_contributors) * 100, 'category_upper':(cat_upper/num_contributors) * 100}
            lst_dict.append(daux)

    final = pd.DataFrame(columns = cols, data = lst_dict)

    category_50 = pd.Series(index=final['timestamp'], data=final['category50%'].values)
    category_80 = pd.Series(index=final['timestamp'], data=final['category80%'].values)
    category_90 = pd.Series(index=final['timestamp'], data=final['category90%'].values)
    category_99 = pd.Series(index=final['timestamp'], data=final['category99%'].values)
    category_upper = pd.Series(index=final['timestamp'], data=final['category_upper'].values)
    category_50.name = "50% of edits"
    category_80.name = "80% of edits"
    category_90.name = "90% of edits"
    category_99.name = "99% of edits"
    category_upper.name = "100% of edits"

    return[category_50, category_80, category_90, category_99, category_upper]
