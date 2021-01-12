FROM ubuntu:bionic

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y tzdata

RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip

WORKDIR /var/wikichron/

COPY ["./install.sh", "."]
COPY ["./requirements.txt", "."]

RUN bash -x install.sh

CMD ["gunicorn", "wikichron_launcher:server", "-c", "gunicorn_config.py"]

# Falta por: * descargar los dumps con docker compose o un script a un directorio determinado y que se usen esos csvs desde ahí. Comprobar con docker antes si está el directorio con los csvs -> necesitaré linkarlos con volumes en docker-compose * traer redis.conf de antiguo servidor


# Para PRODUCCION:
# Acordarse de reestablecer gunicorn_config a los parámetros iniciales (workers) y /data?

#COPY [".", "."] # <- Para produccion + docker ignore
