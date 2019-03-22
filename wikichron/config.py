from wikichron.dash.apps.classic.dash_config import DevelopmentConfig as DashDevelopmentConfig

class DevelopmentConfig(DashDevelopmentConfig):
    PORT = '5002'
    APP_HOSTNAME = f'localhost:{PORT}'
    DASH_STANDALONE = False

