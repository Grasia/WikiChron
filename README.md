# WikiChron
WikiChron is a web tool for the analysis and visualization of the evolution of wiki online communities.

It analyzes the history dump of a wiki and give you nice graphs plotting that data.

# Development

## Install
### Dependencies
* Python 3.5.2 or later
* pip3
* [Dash framework](https://plot.ly/dash)
* [Grasia Dash Components](https://github.com/Grasia/grasia-dash-components)
* [pandas](pandas.pydata.org)
* (Production only) [Redis Cache](https://redis.io/)

### Install instructions
Simply run: `pip3 install -r requirements.txt`

### Using a virtual environment
A good pratice is to use a virtual environment in order to isolate the development environment from your personal stuff. This skips issues about having different Python versions, pip packages in the wrong place or requiring sudo privileges and so on.

In order to do this, first install [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/), either from your package manager or from pip.

Then, create a new virtual environment in the repo root folder with:
`virtualenv -p python3 venv/`

Activate the virtual environment:
`source venv/bin/activate`

And finally, install dependencies here:
`pip install -r requirements.txt`

## XML dumps
Likely, the source data for wikichron will come from a XML file with the full edit history of the wikis you want to analyze. [Go here if you want to learn more about Wikimedia XML dumps](https://www.mediawiki.org/wiki/Manual:Backing_up_a_wiki#Backup_the_content_of_the_wiki_(XML_dump)).

### Get a wiki history dump

First, you will need such xml file. If you don't have shell access to the server you have several options available depending on the wiki you want to download:

- **Wikia wikis**: Supposedly, Wikia automatically generates dumps and provides them for every wiki they host. However, [there is a known bug](http://memory-alpha.wikia.com/wiki/Forum:FYI:_Corrupted_database_backups_(dumps)) in this generation that cuts off the output dumps for large wikis. The best option here is to use [this nice script](https://github.com/Akronix/wikia_dump_downloader) that request and download the complete xml dump through the Special:Export interface. Please, keep in mind that this script does not download all the namespaces available when generating dumps for a wiki, but a wide subset of them ([you can fin more detailed info in the wiki](https://github.com/Grasia/WikiChron/wiki/Basic-concepts#assumptions)).
- **Wikimedia project wikis**: For wikis belonging to the Wikimedia project, you already have a regular updated repo with all the dumps here: http://dumps.wikimedia.org. [Select your target wiki from the list](https://dumps.wikimedia.org/backup-index-bydb.html) and download the complete edit history dump and uncompress it.
- For **other wikis**, like self-hosted wikis, you should use the wikiteam's dumpgenerator.py script. You have a simple tutorial in their wiki: https://github.com/WikiTeam/wikiteam/wiki/Tutorial#I_have_no_shell_access_to_server. Its usage is very straightforward and the script is well maintained. Remember to use the --xml option to download the full history dump.

### Process the dump
Secondly, you'll have to process that xml dump using the script: `dump_parser.py` located in the scripts directory.
In order to do this, place your xml file in the data/ directory and run the following command:

`python3 -m dump_parser data/<name_of_your.xml>`

It will create a new csv file with the same name of your xml in the data/ dir folder.

dump_parser.py also support several xml files at once. For instance, you might want to process all xml files in the data folder:

`python3 -m dump_parser data/*.xml`

## Provide some metadata of the wiki
Wikichron needs one thing else in order to visualize your wiki for you.

You need to have a `wikis.json` file in your data_dir/ directory with some metadata of the wikis you want to explore in wikichron.
That file must have an entry for each wiki with, at least, the following fields: name, url, data, pages number and, optionally, a list of user ids from which you want to remove their activity.
There is an example of `wikis.json` file in the data/ directory of this repo for the given sample set of wikis.

Note that the required information in this file will change in the future. Stay tuned to that file and to the new updates coming.

## Run the application
Use: `python3 -m wikichron` or `python3 wikichron/app.py`

The webapp will be locally available in http://127.0.0.1:8000/app/

Optionally, you can specify a directory with the csv data of the wikis you want to analyze with the environment variable: `WIKICHRON_DATA_DIR`.

For instance, suppose that your data is stored in `/var/tmp`, you might launch wikichron using that directory with:

`WIKICHRON_DATA_DIR='/var/tmp' python3 wikichron/app.py`

It will show all the files ending in .csv as wikis available to analyze and plot.

## Development environment

To get errors messages, backtraces and automatic reloading when source code changes, you must set the environment variable: FLASK_ENV to 'development', i.e.: `export FLASK_ENV=development` prior to launch `app.py`.

You can get more information on this in the [Flask documentation](http://flask.pocoo.org/docs/1.0/server/).

# Deployment
The easiest way is to follow the Dash instructions: https://plot.ly/dash/deployment

There is a script called `deploy.sh` which launches the app with the latest code in master and provides the appropriate arguments. Check it out and modify to suit your needs.

## Setup cache
If you want to run WikiChron in production, you should setup a RedisDB server and add the corresponding parameters to the cache.py file.

Look at the [FlaskCaching documentation](https://pythonhosted.org/Flask-Caching/#rediscache) for more information about caching.


# Third-party licenses

## Font Awesome
We are using icons from the [font-awesome](https://fontawesome.com) repository. These icons are subjected to the Creative Commons Attribution 4.0 International license. [You can find to the terms of their license here](https://fontawesome.com/license).
In particular, we are using the following icons: share-alt-solid, info-circle

### Modifications in font awesome icons
* The file: `share.svg` is a modification of the [`share-alt-solid.svg`](https://fontawesome.com/icons/share-alt?style=solid) file provided by fontawesome.
