ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}-slim-buster

MAINTAINER Nebula Team <users@nebula.org>
LABEL org.opencontainers.image.source=https://github.com/nebulaclouds/nebulakit

WORKDIR /root
ENV PYTHONPATH /root

ARG VERSION
ARG DOCKER_IMAGE

RUN apt-get update && apt-get install build-essential -y \
    && pip install --no-cache-dir -U nebulakit==$VERSION \
        nebulakitplugins-pod==$VERSION \
        nebulakitplugins-deck-standard==$VERSION \
        scikit-learn \
    && apt-get clean autoclean \
    && apt-get autoremove --yes \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/ \
    && useradd -u 1000 nebulakit \
    && chown nebulakit: /root \
    && chown nebulakit: /home \
    && :

USER nebulakit

ENV NEBULA_INTERNAL_IMAGE "$DOCKER_IMAGE"
