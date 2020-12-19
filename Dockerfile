FROM python:3.8.1-slim-buster
ARG alphavantage_api_key

RUN apt-get update
RUN apt-get -y install cron
RUN apt-get -y install curl
RUN apt-get -y install procps
RUN apt-get -y install iputils-ping
RUN apt-get -y install vim
RUN apt-get -y install dos2unix

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /app/database
RUN touch /app/database/tradingbot.db
RUN touch /app/database/tradingbot.sqlite

COPY start.py /app/start.py
COPY start.sh /app/start.sh
COPY src /app/src
COPY templates /app/templates

ENV FLASK_APP=src/main.py
ENV ALPHAVANTAGE_API_KEY=$alphavantage_api_key
RUN chown 664 /app/database
RUN dos2unix start.sh

CMD /app/start.sh