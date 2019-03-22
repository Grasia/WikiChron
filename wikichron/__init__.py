# Python built-in imports
import sys
import os
from flask import Flask

# local imports
from wikichron.config import DevelopmentConfig

# classic app
from wikichron.dash.apps.classic.app import create_dash_app as create_classic, set_up_app as set_up_classic
from wikichron.dash.apps.classic.dash_config import DashConfig as ClassicConfig

def create_app(config_class = DevelopmentConfig):
    print('Creating Flask instance...')
    server = Flask(__name__)

    server.config.from_object(config_class)
    server.config.from_envvar('FLASK_CONFIGURATION', silent=True)

    register_dashapp(server)
    register_blueprints(server)

    return server


def register_dashapp(server):
    server.config.from_object(ClassicConfig)
    classic_dashapp = create_classic(server)
    set_up_classic(classic_dashapp)


def register_blueprints(server):
    from wikichron.flask_app import server_bp

    server.register_blueprint(server_bp)

