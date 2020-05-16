FROM python:3.8-slim

EXPOSE 8000

WORKDIR /dist

COPY ./requirements.txt /dist/requirements.txt

RUN pip install -r /dist/requirements.txt

COPY . /dist/
