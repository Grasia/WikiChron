#!/bin/bash
apt-get update
apt-get install -y python3-tk #Tkinter
#apt-get install -y build-essential python3-dev libxml2 libxml2-dev zlib1g-dev && # deps for python3-igraph
apt-get install -y python3-igraph
pip3 install -r requirements.txt
