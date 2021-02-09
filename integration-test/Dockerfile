FROM docker-registry.knut.univention.de/python:3.9-alpine

RUN mkdir -p /tests

COPY tests /tests/tests
COPY resources /tests/resources
COPY libraries /tests/libraries
COPY requirements.txt /tests/

RUN pip3 install -r /tests/requirements.txt
