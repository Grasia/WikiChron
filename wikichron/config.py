import os

from .version import __version__

DATA_DIR = os.getenv('WIKICHRON_DATA_DIR', 'data')

class DevelopmentConfig(object):
    PORT = '5002'
    APP_HOSTNAME = f'localhost:{PORT}'
    DEBUG = True
    VERSION = __version__
