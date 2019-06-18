# Python built-in imports
import sys
import os
from flask import Flask

# local imports
from wikichron.config import DevelopmentConfig

# classic app
from wikichron.dash.apps.classic.app import create_dash_app as create_classic, set_up_app as set_up_classic
from wikichron.dash.apps.classic.dash_config import register_config as register_classic_config

# networks app
from wikichron.dash.apps.networks.app import create_dash_app as create_networks, set_up_app as set_up_networks
from wikichron.dash.apps.networks.dash_config import register_config as register_networks_config

# monowiki app
from wikichron.dash.apps.monowiki.app import create_dash_app as create_monowiki, set_up_app as set_up_monowiki
from wikichron.dash.apps.monowiki.dash_config import register_config as register_monowiki_config

def create_app(config_class = DevelopmentConfig):
    print('Creating Flask instance...')
    server = Flask(__name__)

    server.config.from_object(config_class)
    if os.environ.get('FLASK_CONFIGURATION'):
        server.config.from_envvar('FLASK_CONFIGURATION')

    register_dashapp(server)
    register_blueprints(server)

    return server


def register_dashapp(server):
    register_classic_config(server.config)
    classic_dashapp = create_classic(server)
    set_up_classic(classic_dashapp)

    register_networks_config(server.config)
    networks_dashapp = create_networks(server)
    set_up_networks(networks_dashapp)


    register_monowiki_config(server.config)
    monowiki_dashapp = create_monowiki(server)
    set_up_monowiki(monowiki_dashapp)


def register_blueprints(server):
    from wikichron.flask_app import server_bp

    server.register_blueprint(server_bp)

