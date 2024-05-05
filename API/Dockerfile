FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /fastapi-app

COPY . .

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

ENTRYPOINT alembic upgrade head && python3 main.py
