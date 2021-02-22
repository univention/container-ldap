ARG BASE_IMAGE_REGISTRY=""
ARG BASE_IMAGE_NAME=python
ARG BASE_IMAGE_TAG=3.9-alpine
FROM ${BASE_IMAGE_REGISTRY}${BASE_IMAGE_NAME}:${BASE_IMAGE_TAG}

COPY requirements.txt /tmp/

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
