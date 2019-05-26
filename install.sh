#!/bin/bash
#apt-get install -y build-essential python-dev libxml2 libxml2-dev zlib1g-dev && # deps for python3-igraph
apt-get install -y python3-igraph && # deps for python3-igraph
pip3 install -r requirements.txt
