from flask_caching import Cache

global cache;
cache = None;

REDIS_URL = 'redis://localhost:6379'

def set_up_cache(app, debug):
    global cache;

    if not debug:
        cache = Cache(app.server, config={
            # try 'filesystem' if you don't want to setup redis
            'CACHE_TYPE': 'redis',
            'CACHE_REDIS_URL': REDIS_URL
        })
    else:
        cache = Cache(app.server, config={'CACHE_TYPE': 'simple'})
