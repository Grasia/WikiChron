from flask_caching import Cache

global cache;
cache = None;

REDIS_URL = 'redis://localhost:6379'

def set_up_cache(app):
    global cache;
    cache = Cache(app.server, config={
        # try 'filesystem' if you don't want to setup redis
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_URL': REDIS_URL
    })
