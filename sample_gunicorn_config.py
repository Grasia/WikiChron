bind = ':80'
timeout = 1200
proc_name = 'WikiChron-networks'
loglevel = 'debug'
errorlog = '-'
workers = 3
raw_env = [
    "WIKICHRON_DATA_DIR=/var/wiki_dumps/csv/",
    "FLASK_ENV=production",
    "FLASK_APP=wikichron_networks.py",
    "FLASK_CONFIGURATION=production_config.cfg"
]



