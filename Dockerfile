FROM python:3.10-slim-buster


WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["sh","scripts/docker-entrypoint.sh"]