FROM ubuntu:bionic
RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install --upgrade pip

WORKDIR /var/wikichron/

COPY [".", "."]

RUN bash install.sh

CMD gunicorn wikichron_launcher:server -c gunicorn_config.py
