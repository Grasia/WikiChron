import sys # TOREPLACE by wikichron.whatever
sys.path.append('wikichron/dash')

from flask import Flask
from config import Config

from wikichron.dash.app import create_dash_app, start_aux_servers, set_up_app


def create_app(config_class = Config):
    print('Creating Flask instance...')
    server = Flask(__name__)
    server.config.from_object(config_class)

    register_dashapp(server)
    register_blueprints(server)

    return server


def register_dashapp(server):
    dashapp = create_dash_app(server)
    set_up_app(dashapp)
    start_aux_servers(dashapp)


def register_blueprints(server):
    from wikichron.flask_app import server_bp

    server.register_blueprint(server_bp)

