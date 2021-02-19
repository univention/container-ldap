ARG BASE_IMAGE_REGISTRY=""
ARG BASE_IMAGE_NAME=python
ARG BASE_IMAGE_TAG=3.9-alpine
FROM ${BASE_IMAGE_REGISTRY}${BASE_IMAGE_NAME}:${BASE_IMAGE_TAG}

RUN mkdir -p /tests

COPY tests /tests/tests
COPY resources /tests/resources
COPY libraries /tests/libraries
COPY requirements.txt /tests/

RUN pip3 install --no-cache-dir -r /tests/requirements.txt
