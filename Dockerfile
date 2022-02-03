FROM python:3.10-alpine
ENV PYTHONUNBUFFERED 1
LABEL org.opencontainers.image.authors="Daniil Rose <daniil.rose@posteo.org>"

RUN apk update && apk upgrade && \
    apk add postgresql-libs postgresql-dev curl libffi-dev openssl-dev build-base

RUN mkdir /code
WORKDIR /code

RUN pip install poetry
COPY . /code/
RUN poetry install
