class BaseConfig(object):
    DASH_BASE_PATHNAME = '/app/'


class DevelopmentConfig(BaseConfig):
    APP_HOSTNAME = 'http://localhost'
    PORT = '8890'
    DEBUG = True
