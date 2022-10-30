FROM python:3.9

WORKDIR /app

COPY api/requirements.txt /app

RUN pip3 install --upgrade pip -r requirements.txt
RUN apt-get update && apt-get install -y netcat

COPY api/. /app
COPY messages /app/messages
COPY utils /app/utils
EXPOSE 5000