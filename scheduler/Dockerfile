FROM python:3.10-slim

WORKDIR /opt
COPY scheduler/requirements.txt .

RUN  apt-get update

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

ENTRYPOINT [ "celery", "-A", "celery_tasks", "worker", "-l", "info", "-B" ]

COPY ./scheduler .
COPY ./broker broker
COPY ./messages messages
COPY ./utils utils
