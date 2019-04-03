"""
   main.py

   Descp: This file is used to control main_view

   Created on: 07-dec-2018

   Copyright 2018-2019 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

# Built-in imports
import os
import time
import json
from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
from urllib.parse import parse_qs, urlencode

# Local imports:
from . import data_controller
from .networks.models import networks_generator as net_factory
from .networks.CytoscapeStylesheet import CytoscapeStylesheet
from .networks.models.BaseNetwork import BaseNetwork
from .main_view import RANKING_EMPTY_DATA, RANKING_EMPTY_HEADER, PAGE_SIZE

TIME_DIV = 60 * 60 * 24 * 30
selection_params = {'wikis', 'network', 'lower_bound', 'upper_bound'}

global debug
debug = True if os.environ.get('FLASK_ENV') == 'development' else False


def update_query_by_time(wiki, query_string, up_val, low_val):
    query_string_dict = parse_qs(query_string)

    # get only the parameters we are interested in for the side_bar selection
    selection = { param: query_string_dict[param] for param in set(query_string_dict.keys()) & selection_params }

    # Let's parse the time values
    first_entry = data_controller.get_first_entry(wiki)
    first_entry = int(datetime.strptime(str(first_entry), "%Y-%m-%d %H:%M:%S").strftime('%s'))
    upper_bound = first_entry + up_val * TIME_DIV
    lower_bound = first_entry + low_val * TIME_DIV

    # Now, time to update the query
    selection['upper_bound'] = upper_bound
    selection['lower_bound'] = lower_bound
    return urlencode(selection,  doseq=True)


def bind_callbacks(app):

    @app.callback(
        Output('network-ready', 'value'),
        [Input('dates-slider', 'value')],
        [State('initial-selection', 'children')]
    )
    def update_network(slider, selection_json):
        if not slider:
            raise PreventUpdate()

        # get network instance from selection
        selection = json.loads(selection_json)
        wiki = selection['wikis'][0]
        network_code = selection['network']

        if debug:
            print(f'Updating network with values:\
            \n\t- wiki: {wiki["url"]}\
            \n\t- network: {network_code}\
            \n\t- slider: ({slider[0]},{slider[1]})')

        print(' * [Info] Building the network....')
        time_start_calculations = time.perf_counter()
        (lower_bound, upper_bound) = data_controller\
                .get_time_bounds(wiki, slider[0], slider[1])
        network = data_controller.get_network(wiki, network_code, lower_bound, upper_bound)

        time_end_calculations = time.perf_counter() - time_start_calculations
        print(f' * [Timing] Network ready in {time_end_calculations} seconds')

        return network.to_cytoscape_dict()


    @app.callback(
        Output('cytoscape', 'stylesheet'),
        [Input('cytoscape', 'elements'),
        Input('tg-show-labels', 'on'),
        Input('tg-show-clusters', 'on'),
        Input('highlight-node', 'value'),
        Input('dd-color-metric', 'value')],
        [State('network-ready', 'value'),
        State('initial-selection', 'children')]
    )
    def update_stylesheet(_, lb_switch, clus_switch, nodes_selc, dd_val,
        cy_network, selection_json):

        if not cy_network:
            raise PreventUpdate()

        selection = json.loads(selection_json)
        network_code = selection['network']

        directed = net_factory.is_directed(network_code)
        stylesheet = CytoscapeStylesheet(directed=directed)
        metric = {}

        if dd_val:
            metric = net_factory.get_secondary_metrics(network_code)[dd_val]

        if not nodes_selc:
            stylesheet.all_transformations(cy_network, metric)
        else:
            stylesheet.highlight_nodes(cy_network, nodes_selc)

        if lb_switch:
            stylesheet.set_label('label')
        else:
            stylesheet.set_label('')

        if clus_switch:
            stylesheet.color_nodes_by_cluster()
        else:
            stylesheet.color_nodes(cy_network, metric)

        return stylesheet.cy_stylesheet


    @app.callback(
        [Output('cytoscape', 'zoom'),
        Output('cytoscape', 'elements')],
        [Input('network-ready', 'value'),
        Input('reset_cyto', 'n_clicks')]
    )
    def add_network_elements(cy_network, _):
        if not cy_network and 'network' not in cy_network:
            raise PreventUpdate()

        return [1, cy_network['network']]


    @app.callback(
        [Output('cytoscape', 'className'),
        Output('no-data', 'className'),
        Output('no-data', 'children')],
        [Input('cytoscape', 'elements')],
        [State('initial-selection', 'children'),
        State('dates-slider', 'value')]
    )
    def check_available_data(cyto, selection_json, slider):
        """
        Checks if there's a network to plot
        """
        if not slider:
            raise PreventUpdate()

        cyto_class = 'show'
        no_data_class = 'non-show'
        no_data_children = []
        if not cyto:
            cyto_class = 'non-show'
            no_data_class = 'show'

            selection = json.loads(selection_json)
            wiki = selection['wikis'][0]
            first_entry = data_controller.get_first_entry(wiki)
            first_entry = int(datetime.strptime(str(first_entry), "%Y-%m-%d %H:%M:%S").strftime('%s'))
            upper_bound = first_entry + slider[1] * TIME_DIV
            lower_bound = first_entry + slider[0] * TIME_DIV
            upper_bound = datetime.fromtimestamp(upper_bound).strftime('%B/%Y')
            lower_bound = datetime.fromtimestamp(lower_bound).strftime('%B/%Y')

            no_data_children = [
                html.P('Nothing to show,'),
                html.P(f'no data available between {lower_bound} and {upper_bound}.'),
                html.P('Please, try changing the date selection.')
            ]

        return cyto_class, no_data_class, no_data_children


    @app.callback(
        Output('share-dialog', 'open'),
        [Input('share-button', 'n_clicks')],
        [State('share-dialog', 'open')]
    )
    def show_share_modal(n_clicks: int, open_state: bool):
        if not n_clicks: # modal init closed
            return False
        elif n_clicks > 0 and not open_state: # opens if we click and `open` state is not open
            return True
        else: # otherwise, leave it closed.
            return False

        return # bind_callbacks


    @app.callback(
        [Output('date-slider-container', 'children'),
        Output('first-entry-signal', 'children')],
        [Input('initial-selection', 'children')],
        [State('url', 'search')]
    )
    def update_slider(selection_json, query_string):
         # get network instance from selection
        selection = json.loads(selection_json)
        wiki = selection['wikis'][0]

        # Attention! query_string includes heading ? symbol
        query_string_dict = parse_qs(query_string[1:])

        # get only the parameters we are interested in for the side_bar selection
        selection = { param: query_string_dict[param] for param in set(query_string_dict.keys()) & selection_params }

        origin = data_controller.get_first_entry(wiki)
        end = data_controller.get_last_entry(wiki)

        origin = int(datetime.strptime(str(origin),
            "%Y-%m-%d %H:%M:%S").strftime('%s'))
        end = int(datetime.strptime(str(end),
            "%Y-%m-%d %H:%M:%S").strftime('%s'))

        time_gap = end - origin
        max_time = time_gap // TIME_DIV

        if all(k in selection for k in ('lower_bound', 'upper_bound')):
            low_val = (int(selection['lower_bound'][0]) - origin) // TIME_DIV
            upper_val = (int(selection['upper_bound'][0]) - origin) // TIME_DIV
        else:
            low_val = 1
            upper_val = int(2 + max_time / 10)

        if max_time < 12:
            step_for_marks = 1
        elif max_time < 33:
            step_for_marks = 3
        elif max_time < 66:
            step_for_marks = 6
        elif max_time < 121:
            step_for_marks = 12
        elif max_time < 264:
            step_for_marks = 24
        else:
            step_for_marks = 36

        range_slider_marks = {i: datetime.fromtimestamp(origin
         + i * TIME_DIV).strftime('%b %Y') for i in range(1,
         max_time-step_for_marks, step_for_marks)}

        range_slider_marks[max_time] = datetime.fromtimestamp(
        origin + max_time * TIME_DIV).strftime('%b %Y')

        return  dcc.RangeSlider(
                    id='dates-slider',
                    min=1,
                    max=max_time,
                    step=1,
                    value=[low_val, upper_val],
                    marks=range_slider_marks
                ), origin


    @app.callback(
        Output('dates-slider', 'value'),
        [Input('bt-back', 'n_clicks_timestamp'),
        Input('bt-forward', 'n_clicks_timestamp')],
        [State('in-step-slider', 'value'),
        State('date-slider-container', 'children')]
    )
    def move_slider_range(bt_back, bt_forward, step, di_slider):
        """
        Controls to move the slider selection
        """
        if not step:
            raise PreventUpdate()

        step = int(step)

        if bt_back and int(bt_back) > int(bt_forward):
            step = -step
        elif not (bt_forward and int(bt_forward) > int(bt_back)):
            raise PreventUpdate()

        # step value is in [0, n] | n € N
        # if bt_forward is pressed, the step value will be a positive value

        old_upper = di_slider['props']['value'][0]
        old_lower = di_slider['props']['value'][1]
        upper = di_slider['props']['value'][0]
        lower = di_slider['props']['value'][1]
        max_val = di_slider['props']['max']
        min_val = di_slider['props']['min']

        if upper + step > max_val:
            upper = max_val
        elif upper + step < min_val:
            upper = min_val
        else:
            upper = upper + step

        if lower + step < min_val:
            lower = min_val
        elif lower + step > max_val:
            lower = max_val
        else:
            lower = lower + step
        # Let's check if the input will change the slider
        if lower == old_lower and upper == old_upper:
             raise PreventUpdate('Slider will not change')

        return [upper, lower]


    @app.callback(
        Output('download-button', 'href'),
        [Input('dates-slider', 'value')],
        [State('download-button', 'href'),
        State('initial-selection', 'children')]
    )
    def update_download_url(slider, query_string, selection_json):
        if not slider:
            raise PreventUpdate()
        selection = json.loads(selection_json)
        wiki = selection['wikis'][0]

        query_splited = query_string.split("?")
        new_query = update_query_by_time(wiki, query_splited[1], slider[1], slider[0])
        href = f'{query_splited[0]}?{new_query}'

        if debug:
            print(f'Download href updated to: {href}')

        return href


    @app.callback(
        Output('share-link-input', 'value'),
        [Input('dates-slider', 'value')],
        [State('share-link-input', 'value'),
        State('initial-selection', 'children')]
    )
    def update_share_url(slider, query_string, selection_json):
        if not slider:
            raise PreventUpdate()
        selection = json.loads(selection_json)
        wiki = selection['wikis'][0]

        query_splited = query_string.split("?")
        new_query = update_query_by_time(wiki, query_splited[1], slider[1], slider[0])
        new_query = f'{query_splited[0]}?{new_query}'
        if debug:
            print(f'Share link updated to: {new_query}')

        return new_query


    @app.callback(
        Output('distribution-graph', 'figure'),
        [Input('scale', 'value'),
        Input('dates-slider', 'value')],
        [State('initial-selection', 'children')]
    )
    def update_graph(scale_type, slider, selection_json):
        if not slider:
            raise PreventUpdate()

        selection = json.loads(selection_json)
        wiki = selection['wikis'][0]
        network_code = selection['network']
        (lower, upper) = data_controller.get_time_bounds(wiki, slider[0], slider[1])
        network = data_controller.get_network(wiki, network_code, lower, upper)

        (k, p_k) = network.get_degree_distribution()

        return {
            'data': [go.Scatter(
                x=k,
                y=p_k,
                mode='markers',
                marker={
                    'size': 15,
                    'opacity': 0.5,
                    'line': {'width': 0.5, 'color': 'white'}
                }
            )],
            'layout': go.Layout(
                xaxis={
                    'title': 'K',
                    'type': 'linear' if scale_type == 'Linear' else 'log'
                },
                yaxis={
                    'title': 'P_k',
                    'type': 'linear' if scale_type == 'Linear' else 'log'
                },
                margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
                hovermode='closest'
            )
        }


    @app.callback(
        Output('net-stats', 'children'),
        [Input('network-ready', 'value')]
    )
    def update_network_stats(cy_network):
        if not cy_network:
            raise PreventUpdate()

        stats = BaseNetwork.get_network_stats()
        child = []
        i = 0
        group = []
        for k, val in stats.items():
            group.append(html.Div(children=[
                html.P(f'{k}:'),
                html.P(cy_network[val])
            ]))

            i += 1
            if i % 2 == 0:
                child.append(html.Div(children=group))
                group = []

        return child


    @app.callback(
        Output('ranking-table', 'columns'),
        [Input('dd-local-metric', 'value'),
        Input('network-ready', 'value')],
        [State('initial-selection', 'children')]
    )
    def update_ranking_header(metric, ready, selection_json):
        if not ready:
            if debug:
                print('not ready header')
            raise PreventUpdate()

        if not metric:
            return RANKING_EMPTY_HEADER

        selection = json.loads(selection_json)
        network_code = selection['network']
        header = net_factory.get_metric_header(network_code, metric)

        if not header:
            raise PreventUpdate()
        return header


    @app.callback(
        Output('ranking-table', 'data'),
        [Input('ranking-table', 'pagination_settings'),
        Input('ranking-table', 'sorting_settings'),
        Input('dd-local-metric', 'value'),
        Input('network-ready', 'value')],
        [State('dates-slider', 'value'),
        State('initial-selection', 'children')]
    )
    def update_ranking(pag_set, sort_set, metric, ready, slider, selection_json):
        if not ready or not slider:
            raise PreventUpdate()

        data = RANKING_EMPTY_DATA.to_dict('rows')
        data_keys = RANKING_EMPTY_DATA.columns

        if metric:
            selection = json.loads(selection_json)
            wiki = selection['wikis'][0]
            network_code = selection['network']
            (lower, upper) = data_controller.get_time_bounds(wiki, slider[0], slider[1])
            network = data_controller.get_network(wiki, network_code, lower, upper)

            df = network.get_metric_dataframe(metric)

            if not df.empty:
                # check the col to sort
                if sort_set and sort_set[0]['column_id'] in list(df):
                    df = df.sort_values(sort_set[0]['column_id'],
                        ascending=sort_set[0]['direction'] == 'asc',
                        inplace=False)
                else:
                    df = df.sort_values(metric, ascending=False)

                data_keys = df.columns
                data = df.iloc[
                        pag_set['current_page']*pag_set['page_size']:
                        (pag_set['current_page'] + 1)*pag_set['page_size']
                    ].to_dict('rows')

        # fill with empty rows
        for _ in range(0, PAGE_SIZE - len(data)):
            empty_dict = {}
            for k in data_keys:
                empty_dict[k] = ''
            data.append(empty_dict)

        return data


    @app.callback(
        Output('highlight-node', 'value'),
        [Input('ranking-table', 'derived_virtual_data'),
        Input('ranking-table', 'derived_virtual_selected_rows')]
    )
    def highlight_node(data, selected):
        if not data:
            raise PreventUpdate()

        # Reset the stylesheet
        if not selected:
            return None

        # highlight nodes selected
        selection = [data[s] for s in selected]

        # filter empty rows
        selc_filtered = []
        for s in selection:
            keys = list(s.keys())
            if s[keys[0]]:
                selc_filtered.append(s)

        if not selc_filtered:
            raise PreventUpdate()

        return selection


    @app.callback(
        Output('ranking-table', 'selected_rows'),
        [Input('dd-local-metric', 'value')]
    )
    def clear_ranking_selection(_):
        return []


    @app.callback(
        Output('user-stats', 'children'),
        [Input('cytoscape', 'tapNodeData')],
        [State('initial-selection', 'children')]
    )
    def update_node_info(user_info, selection_json):
        if not user_info:
            raise PreventUpdate()

        selection = json.loads(selection_json)
        network_code = selection['network']
        dic_info = net_factory.get_user_info(network_code)
        dic_metrics = net_factory.get_available_metrics(network_code)

        info_stack = []
        # Let's add the user info
        for key in dic_info.keys():
            if dic_info[key] in user_info:
                info_stack.append(html.Div(children=[
                    html.P(f'{key}:'),
                    html.P(user_info[dic_info[key]])
                ], className='user-container-stat'))

        # Let's add the metrics
        for key in dic_metrics.keys():
            if dic_metrics[key] in user_info:
                info_stack.append(html.Div(children=[
                    html.P(f'{key}:'),
                    html.P(user_info[dic_metrics[key]])
                ], className='user-container-stat'))

        return info_stack


    @app.callback(
        Output('caption', 'className'),
        [Input('tg-hide-caption', 'on')]
    )
    def hide_caption(switch):
        _class = 'pane caption'
        if switch:
            _class = 'pane non-show'
        return _class