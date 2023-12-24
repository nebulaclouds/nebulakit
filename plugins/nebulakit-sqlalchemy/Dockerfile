ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}-slim-buster

WORKDIR /root
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /root

ARG VERSION
ARG JFROG_USER
ARG JFROG_PASSWORD

RUN pip install sqlalchemy \
		psycopg2-binary \
		pymysql
RUN pip install --no-cache-dir -U \
      --index https://$JFROG_USER:$JFROG_PASSWORD@streamlineio.jfrog.io/artifactory/api/pypi/nebula-pypi/simple \
      --extra-index-url https://pypi.python.org/simple \
      nebulakit nebulakitplugins-sqlalchemy

#		nebulakitplugins-sqlalchemy==$VERSION \
#		nebulakit==$VERSION

RUN useradd -u 1000 nebulakit
RUN chown nebulakit: /root
USER nebulakit
