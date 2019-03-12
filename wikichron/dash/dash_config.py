class BaseConfig(object):
    DASH_BASE_PATHNAME = '/app/'
    DASH_DOWNLOAD_PATHNAME = '/download/'


class DevelopmentConfig(BaseConfig):
    PORT = '8890'
    APP_HOSTNAME = f'http://localhost:{PORT}'
    DEBUG = True
