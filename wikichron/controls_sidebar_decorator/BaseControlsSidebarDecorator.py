"""
   BaseControlsSidebarDecorator.py

   Descp: A class to implement the decorator pattern in order to make an
     easier implementation of the right sidebar

   Created on: 08-02-2019

   Copyright 2019 Youssef 'FRYoussef' El Faqir el Rhazoui <f.r.youssef@hotmail.com>
"""

import abc
from .ControlsSidebar import ControlsSidebar


class BaseControlsSidebarDecorator(ControlsSidebar, metaclass=abc.ABCMeta):

    def __init__(self, sidebar):
        self.sidebar = sidebar


    def add_stats_section(self):
        self.sidebar.add_stats_section()


    def add_stats_content(self, html_stats):
        self.sidebar.add_stats_content(html_stats)


    def add_metrics_section(self):
        self.sidebar.add_metrics_section()


    def add_metrics_content(self, html_metrics):
        self.sidebar.add_metrics_content(html_metrics)


    def add_options_section(self):
        self.sidebar.add_options_section()


    def add_options_content(self, html_options):
        self.sidebar.add_options_content(html_options)


    def add_all_sections(self):
        self.sidebar.add_all_sections()