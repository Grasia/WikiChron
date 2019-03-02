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


    def add_stats_section(self, stats_content):
        self.sidebar.add_stats_section(stats_content)


    def add_options_section(self, options_content):
        self.sidebar.add_options_section(options_content)


    def add_all_sections(self, stats_content, options_content):
        self.sidebar.add_all_sections(stats_content, options_content)


    @abc.abstractclassmethod
    def bind_callbacks(cls, app):
        pass
