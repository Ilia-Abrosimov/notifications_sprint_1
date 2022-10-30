FROM python:3.10

WORKDIR /opt/app/
COPY worker/requirements.txt .

RUN  pip3 install --upgrade pip \
     && pip3 install -r requirements.txt --no-cache-dir

COPY broker ./broker
COPY messages ./messages
COPY worker/main.py .
COPY worker ./worker
COPY utils ./utils
