from .version import __version__

class DevelopmentConfig(object):
    PORT = '5002'
    APP_HOSTNAME = f'localhost:{PORT}'
    DEBUG = True
    VERSION = __version__

