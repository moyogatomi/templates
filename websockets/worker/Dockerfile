FROM python:3.7-slim-stretch

ENV APP dramaworker
ENV APPDIR /app/$APP
ENV PYTHONPATH=$APPDIR:$APPDIR/
WORKDIR $APPDIR

RUN \
  apt-get update && \
  apt-get install -y --no-install-recommends \
  build-essential \
  net-tools \
  nginx \
  runit && \
  apt-get -y autoremove && \
  apt-get clean

COPY ./requirements.txt requirements.txt

RUN \
  pip install --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt && \
  apt-get -y remove build-essential && \
  apt-get -y autoremove && \
  apt-get clean

RUN useradd worker

COPY . .
COPY ./dramatiq_conf.py dramatiq_conf.py
