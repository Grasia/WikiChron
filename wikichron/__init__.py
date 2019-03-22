import sys
import os
from flask import Flask

from wikichron.dash.apps.classic.app import create_dash_app, set_up_app
from wikichron.config import DevelopmentConfig

def create_app(config_class = DevelopmentConfig):
    print('Creating Flask instance...')
    server = Flask(__name__)

    server.config.from_object(config_class)
    server.config.from_envvar('FLASK_CONFIGURATION', silent=True)

    register_dashapp(server)
    register_blueprints(server)

    return server


def register_dashapp(server):
    dashapp = create_dash_app(server)
    set_up_app(dashapp)


def register_blueprints(server):
    from wikichron.flask_app import server_bp

    server.register_blueprint(server_bp)

