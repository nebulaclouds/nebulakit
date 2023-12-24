ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}-slim-buster

MAINTAINER Nebula Team <users@nebula.org>
LABEL org.opencontainers.image.source=https://github.com/nebulaclouds/nebulakit

WORKDIR /root
ENV PYTHONPATH /root

ARG VERSION
ARG DOCKER_IMAGE

RUN apt-get update
RUN apt-get dist-upgrade -y
RUN apt-get install -y curl rsync
RUN curl -fL https://install-cli.jfrog.io | sh

#RUN jf pipc --global --repo-resolve="nebula-pypi"
#RUN jf pip install nebulakit

COPY ./ packages/

RUN apt-get update && apt-get install build-essential -y \
    && pip install --no-cache-dir -U packages \
    && pip install --no-cache-dir -U packages/plugins/nebulakit-deck-standard \
    && pip install --no-cache-dir -U packages/plugins/nebulakit-k8s-pod \
    && pip install --no-cache-dir -U scikit-learn \
    && apt-get clean autoclean \
    && apt-get autoremove --yes \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/ \
    && useradd -u 1000 nebulakit \
    && chown nebulakit: /root \
    && chown nebulakit: /home \
    && :

USER nebulakit

ENV NEBULA_INTERNAL_IMAGE "$DOCKER_IMAGE"
