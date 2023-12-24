ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}-slim-buster

MAINTAINER Nebula Team <users@nebula.org>
LABEL org.opencontainers.image.source=https://github.com/nebulaclouds/nebulakit

WORKDIR /root
ENV PYTHONPATH /root

ARG VERSION
ARG DOCKER_IMAGE
ARG JFROG_USER
ARG JFROG_PASSWORD

RUN apt-get update && apt-get install build-essential -y \
    && pip install --no-cache-dir -U \
      --index https://$JFROG_USER:$JFROG_PASSWORD@streamlineio.jfrog.io/artifactory/api/pypi/nebula-pypi/simple \
      --extra-index-url https://pypi.python.org/simple \
      nebulakit nebulakitplugins-pod nebulakitplugins-deck-standard    \
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
