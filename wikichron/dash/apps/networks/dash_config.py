class BaseConfig(object):
    DASH_BASE_PATHNAME = '/app/'
    DASH_DOWNLOAD_PATHNAME = '/download/'
    DASH_STANDALONE = True


class DevelopmentConfig(BaseConfig):
    PORT = '8890'
    APP_HOSTNAME = f'localhost:{PORT}'
    DEBUG = True
