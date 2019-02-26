from flask import Flask

from app import create_dash_app, set_up_app, start_aux_servers, run

server = Flask(__name__)

# create and config Dash instance
app = create_dash_app(server)

# set layout, import startup js and bind callbacks
set_up_app(app)

# init auxiliar servers & deps
start_aux_servers(app)

run(app)
