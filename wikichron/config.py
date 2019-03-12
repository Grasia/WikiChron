from wikichron.dash.dash_config import DevelopmentConfig as DashDevelopmentConfig

class DevelopmentConfig(DashDevelopmentConfig):
    PORT = '5000'
    APP_HOSTNAME = f'http://localhost:{PORT}'

