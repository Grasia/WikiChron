from flask import Config

from . import WIKICHRON_APP_NAME

classic_config = {
    'DASH_BASE_PATHNAME': '/classic/app/',
    'DASH_DOWNLOAD_PATHNAME': '/classic/download/',
    'DASH_STANDALONE': False
}


def register_config(config: Config):
    config[WIKICHRON_APP_NAME] = classic_config


# DEPRECATED
# Meant to be used in run_standalone_dashapp.sh
class DevelopmentConfig(object):
    PORT = '8880'
    APP_HOSTNAME = f'localhost:{PORT}'
    DEBUG = True
    CLASSIC = {
        'DASH_BASE_PATHNAME': '/classic/app/',
        'DASH_DOWNLOAD_PATHNAME': '/classic/download/',
        'DASH_STANDALONE': True
    }
