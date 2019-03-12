# WikiChron-networks
WikiChron is a web tool for the analysis and visualization of the evolution of wiki online communities.

This flavour of WikiChron will show you insightful visualizations of wikis in the shape of networks.

# Development

## Install
### Dependencies
* Python 3.6.7 or later
* pip3
* [Dash framework](https://plot.ly/dash)
* [Grasia Dash Components](https://github.com/Grasia/grasia-dash-components)
* [pandas](pandas.pydata.org)
* (Production only) [Redis Cache](https://redis.io/)
* [python-igraph] (https://igraph.org/python/) -> it's a c package so it depends on your OS

### Install instructions
The dependency `python-igraph` needs to compile some C code, so, in order to install it, you priorly need some dev libraries for python, xml, zlib and C compiler utilities.

For Ubuntu 16.04/18.04 and derivatives, you can use the following command to install those:

`sudo apt-get install build-essential python3-dev libxml2 libxml2-dev zlib1g-dev`

After that, simply run: `pip3 install -r requirements.txt`. pip will install (and build for the case of python-igraph) all the dependencies you need.

### Using a virtual environment
A good pratice is to use a virtual environment in order to isolate the development environment from your personal stuff. This skips issues about having different Python versions, pip packages in the wrong place or requiring sudo privileges and so on.

In order to do this, first install [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/), either from your package manager or from pip.

Then, create a new virtual environment in the repo root folder with:
`virtualenv -p python3 venv/`

Activate the virtual environment:
`source venv/bin/activate`

And finally, install dependencies here:
`pip install -r requirements.txt`

## Input wiki data
Likely, the source data for wikichron will come from a XML file with the full edit history of the wikis you want to analyze. [Go here if you want to learn more about Wikimedia XML dumps](https://www.mediawiki.org/wiki/Manual:Backing_up_a_wiki#Backup_the_content_of_the_wiki_(XML_dump).

In order to get such XML dump, [you can follow the instructions explained in the WikiChron's wiki](https://github.com/Grasia/WikiChron/wiki/How-to-add-a-new-wiki#get-the-dump).

### Process the dump
Secondly, you'll need to convert that xml raw data into a processed csv that WikiChron can load and work with.

For that transformation, you should use our [wiki-dump-parser script](https://pypi.org/project/wiki-dump-parser/). You can find a short guide on how to use this script [in this page of the WikiChron's wiki](https://github.com/Grasia/WikiChron/wiki/How-to-add-a-new-wiki#process-the-dump).

## Provide some metadata of the wiki
Wikichron needs one last thing in order to serve the visualization of a wiki for you.

You need to have a `wikis.json` file in your data_dir/ directory with some metadata of the wikis you want to explore; like the number of pages, the number of users, the user ids of the bots, etc.

You can find some helpful instructions on how to edit or automatically generate this file using a script [in this page of the WikiChron's wiki](https://github.com/Grasia/WikiChron/wiki/How-to-add-a-new-wiki#modify-the-wikisjson-file).

## Run the application
Use: `FLASK_ENV=development python3 -m wikichron.dash`

The webapp will be locally available under http://127.0.0.1:8890/app/

Optionally, you can specify a directory with the csv data of the wikis you want to analyze with the environment variable: `WIKICHRON_DATA_DIR`.

For instance, suppose that your data is stored in `/var/tmp`, you might launch wikichron using that directory with:

`WIKICHRON_DATA_DIR='/var/tmp' FLASK_ENV=development python -m wikichron.dash`

It will show all the files ending in .csv as wikis available to analyze and plot.

## Development environment

To get errors messages, backtraces and automatic reloading when source code changes, you must set the environment variable: FLASK_ENV to 'development', i.e.: `export FLASK_ENV=development` prior to launch `app.py`.

There is a simple but handy script called `run_develop.sh` which set the app for development environment and launches it locally.

You can get more information on this in the [Flask documentation](http://flask.pocoo.org/docs/1.0/server/).

# Deployment
The easiest way is to follow the Dash instructions: https://plot.ly/dash/deployment

There is a script called `deploy.sh` which launches the app with the latest code in master and provides the appropriate arguments. Check it out and modify to suit your needs.

## gunicorn config

For the deployment you need to set some configuration in a file called `gunicorn_config.py`.

You can start by copying the sample config file located in this repo and then edit the config parameters needed to suit your specific needs:

`cp sample_gunicorn_config.py gunicorn_config.py`

The documentation about the gunicorn settings allowed in this file can be found [in the official gunicorn documentation](https://docs.gunicorn.org/en/stable/settings.html#settings).

The environment variable `WIKICHRON_DATA_DIR` is bypassed directly to WikiChron and sets the directory where WikiChron will look for the wiki data files, as it was explained previously in the [Run the application section](#run-the-application).

## Setup cache
If you want to run WikiChron in production, you should setup a RedisDB server and add the corresponding parameters to the cache.py file.

Look at the [FlaskCaching documentation](https://pythonhosted.org/Flask-Caching/#rediscache) for more information about caching.


# Third-party licenses

## External libs
This project use several external javascript libraries and fonts. Their source code is included under the lib/ folder for its usage in development, however each one of them is subjected to their corresponding license.
The usage of those in producion is linked using a CDN service.

## Font Awesome
We are using icons from the [font-awesome](https://fontawesome.com) repository. These icons are subjected to the Creative Commons Attribution 4.0 International license. [You can find to the terms of their license here](https://fontawesome.com/license).
In particular, we are using the following icons: share-alt-solid, info-circle

### Modifications in font awesome icons
* The file: `share.svg` is a modification of the [`share-alt-solid.svg`](https://fontawesome.com/icons/share-alt?style=solid) file provided by fontawesome.
