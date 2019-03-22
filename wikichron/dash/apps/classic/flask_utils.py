#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   flask_utils.py

   Descp:

   Created on: 22-mar-2019

   Copyright 2019 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""
from . import WIKICHRON_APP_NAME
from flask import Flask

def get_app_config(server: Flask):
   return server.config[WIKICHRON_APP_NAME]

