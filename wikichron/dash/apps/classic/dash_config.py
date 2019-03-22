class DashConfig(object):
    DASH_BASE_PATHNAME = '/classic/'
    DASH_DOWNLOAD_PATHNAME = f'{DASH_BASE_PATHNAME}download/'

class DevelopmentConfig(DashConfig):
    PORT = '8880'
    APP_HOSTNAME = f'localhost:{PORT}'
    DEBUG = True
    DASH_STANDALONE = True
