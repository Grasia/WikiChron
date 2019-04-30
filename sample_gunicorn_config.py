import multiprocessing

bind = ':80'
timeout = 1200
proc_name = 'WikiChron'
loglevel = 'debug'
errorlog = '-'
workers = multiprocessing.cpu_count() * 2 + 1 # example in gunicorn docs 
raw_env = [
    "WIKICHRON_DATA_DIR=/data/wiki_dumps/csv/",
    "FLASK_ENV=production",
    "FLASK_APP=wikichron_launcher.py",
    "FLASK_CONFIGURATION=production_config.cfg"
]



