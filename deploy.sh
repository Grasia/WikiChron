(git pull origin master && pkill -HUP gunicorn) ||
$(WIKICHRON_DATA_DIR='/var/wiki_dumps/csv/' gunicorn app:server -b :80 -t 600)
