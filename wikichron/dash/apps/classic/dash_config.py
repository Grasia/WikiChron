from flask import Config

from . import WIKICHRON_APP_NAME

HOME_MODE_PATHNAME = '/classic/'
DASH_STATIC_FOLDER = 'resources'

classic_config = {
    'HOME_MODE_PATHNAME': HOME_MODE_PATHNAME,
    'DASH_BASE_PATHNAME': f'{HOME_MODE_PATHNAME}app/',
    'DASH_DOWNLOAD_PATHNAME': f'{HOME_MODE_PATHNAME}download/',
    'DASH_STANDALONE': False,
    'DASH_STATIC_FOLDER': DASH_STATIC_FOLDER,
    'DASH_STATIC_PATHNAME': f'{HOME_MODE_PATHNAME}app/{DASH_STATIC_FOLDER}'
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
        'HOME_MODE_PATHNAME': HOME_MODE_PATHNAME,
        'DASH_BASE_PATHNAME': f'{HOME_MODE_PATHNAME}app/',
        'DASH_DOWNLOAD_PATHNAME': f'{HOME_MODE_PATHNAME}download/',
        'DASH_STANDALONE': True
    }
