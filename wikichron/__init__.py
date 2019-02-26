import sys
from flask import Flask
from config import Config

# Comes back absolute imports like in python2.
# This means that you can do local imports as if they were absolute from
#   source files as long as they are within the dash/ directory.
# For instance, you can do `import main` inside wikichron/dash/app.py
#   instead of `import wikichron.dash.main`
# Note that, if we had to do `import wikichron.dash.main` we could not run
#  the dash app as an standalone app for developing and testing, but we had to
# run the full Flask + Dash altogether.
sys.path.append('wikichron/dash')

from wikichron.dash.app import create_dash_app, set_up_app

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


def register_blueprints(server):
    from wikichron.flask_app import server_bp

    server.register_blueprint(server_bp)

