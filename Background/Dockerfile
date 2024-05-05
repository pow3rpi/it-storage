FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /celery-app

COPY . .

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

ENTRYPOINT celery -A src.entrypoints.worker worker --loglevel=DEBUG
