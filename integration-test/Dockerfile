ARG DOCKERHUB_CACHE=artifacts.knut.univention.de/dockerhub_proxy_cache/library/
ARG BASE_IMAGE_NAME=python
ARG BASE_IMAGE_TAG=3.9-alpine
FROM ${DOCKERHUB_CACHE}${BASE_IMAGE_NAME}:${BASE_IMAGE_TAG}

COPY requirements.txt /tmp/

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
