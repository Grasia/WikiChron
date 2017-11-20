# WikiChron
Data visualization tool for wikis.

It analyzes the history dump of a wiki and give you nice graphs plotting that data.

## Dependencies
* Python 3.5.2 or later
* [Dash framework](https://plot.ly/dash)

## Usage

First, download a xml file with the full history of the wikis you want to analyze (you can use [this nice script](https://github.com/Akronix/wikia_dump_downloader) to do so).

Second, you'll have to process that xml dump using the script: `dump_parser.py` located in the scripts directory.
In order to do this, place your xml file in the data/ directory and run the following command:

`python3 dump_parser.py data/<name_of_your.xml>`

It will create a new csv file with the same name of your xml in the data/ dir folder.

dump_parser.py also support several xml files at once. For instance, you might want to process all xml files in the data folder:

`python3 dump_parser.py data/*.xml`
