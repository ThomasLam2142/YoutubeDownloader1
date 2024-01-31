FROM python:3-alpine

ENV APP_HOME /app
WORKDIR $APP_HOME

RUN apk update && apk add ffmpeg

RUN pip install moviepy

RUN pip install numpy

RUN pip install pytube


RUN pip install Flask requests gevent
COPY . $APP_HOME


CMD ["python", "main.py"]
