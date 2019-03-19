from wikichron.dash.dash_config import DevelopmentConfig as DashDevelopmentConfig

class DevelopmentConfig(DashDevelopmentConfig):
    PORT = '5001'
    APP_HOSTNAME = f'localhost:{PORT}'
    DASH_STANDALONE = False

