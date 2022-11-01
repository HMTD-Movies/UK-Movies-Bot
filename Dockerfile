FROM python:3.10-slim-buster

RUN apt update && apt upgrade -y
RUN apt install git -y
COPY requirements.txt /requirements.txt

RUN mkdir /app/
COPY . /app
WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install -U -r requirements.txt

CMD python3 bot.py
