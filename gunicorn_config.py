bind = ':80'
timeout = 1200
proc_name = 'WikiChron'
loglevel = 'debug'
errorlog = '-'
raw_env = [
	"WIKICHRON_DATA_DIR=/var/wiki_dumps/csv/"
]



