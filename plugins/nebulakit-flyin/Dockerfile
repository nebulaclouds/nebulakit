ARG PYTHON_VERSION
FROM python:3.10-slim-buster
MAINTAINER Nebula Team <users@nebula.org>
LABEL org.opencontainers.image.source https://github.com/nebulaclouds/nebulakit
WORKDIR /root
ENV PYTHONPATH /root

ARG VERSION
ARG TARGETARCH
ARG JFROG_USER
ARG JFROG_PASSWORD

RUN apt-get update \
    && apt-get install build-essential git wget -y \
    && mkdir -p /tmp/ \
    && mkdir -p /tmp/code-server \
    && wget --no-check-certificate -O /tmp/code-server/code-server-4.19.0-linux-${TARGETARCH}.tar.gz https://github.com/coder/code-server/releases/download/v4.19.0/code-server-4.19.0-linux-${TARGETARCH}.tar.gz \
    && tar -xzf /tmp/code-server/code-server-4.19.0-linux-${TARGETARCH}.tar.gz -C /tmp/code-server/ \
    && wget --no-check-certificate https://open-vsx.org/api/ms-python/python/2023.20.0/file/ms-python.python-2023.20.0.vsix -P /tmp/code-server \
    && wget --no-check-certificate https://open-vsx.org/api/ms-toolsai/jupyter/2023.9.100/file/ms-toolsai.jupyter-2023.9.100.vsix -P /tmp/code-server \
    && pip install --no-cache-dir -U \
      --index https://$JFROG_USER:$JFROG_PASSWORD@streamlineio.jfrog.io/artifactory/api/pypi/nebula-pypi/simple \
      --extra-index-url https://pypi.python.org/simple \
      nebulakit-flyin nebulakit \
    && apt-get clean autoclean \
    && apt-get autoremove --yes \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/ \
    && useradd -u 1000 nebulakit \
    && chown nebulakit: /root \
    && chown nebulakit: /home \
    && :

# Set the environment variable for code-server
ENV PATH="/tmp/code-server/code-server-4.19.0-linux-${TARGETARCH}/bin:${PATH}"

USER nebulakit

RUN code-server --install-extension /tmp/code-server/ms-python.python-2023.20.0.vsix \
    && code-server --install-extension /tmp/code-server/ms-toolsai.jupyter-2023.9.100.vsix
