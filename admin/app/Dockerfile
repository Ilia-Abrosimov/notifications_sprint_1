FROM python:3.10

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY messages ./messages
COPY broker ./broker
COPY utils ./utils

COPY admin/app/run_uwsgi.sh run_uwsgi.sh
COPY admin/app/requirements.txt ./
COPY admin/app/requirements ./requirements
COPY admin/app/uwsgi/uwsgi.ini uwsgi.ini

RUN  mkdir -p /opt/app/static/ \
     && mkdir -p /opt/app/media/ \
     && pip3 install --upgrade pip \
     && pip3 install -r requirements.txt --no-cache-dir

RUN groupadd varwwwusers \
    && adduser www-data varwwwusers \
    && chgrp -R varwwwusers /opt/app/ \
    && chmod -R 770 /opt/app/

COPY admin/app/. .

EXPOSE 8000

ENTRYPOINT ["uwsgi", "--strict", "--ini", "uwsgi.ini"]
