FROM continuumio/miniconda3:latest

ENV PYTHONUNBUFFERED 1

RUN apt-get --allow-releaseinfo-change update && \
    apt-get -y install gcc libpq-dev libmagic1 && \
    rm -rf /var/lib/apt/lists/*

ADD https://github.com/krallin/tini/releases/download/v0.19.0/tini /sbin/tini
RUN chmod +x /sbin/tini

RUN mkdir /app
ADD . /app/
WORKDIR /app
RUN conda env create --name annotation-tool --file environment.yml
RUN conda install --name annotation-tool gunicorn

COPY package.json package-lock.json ./
COPY frontend/package.json frontend/package-lock.json frontend/

SHELL ["conda", "run", "-n", "annotation-tool", "/bin/bash", "-c"]

RUN npm install --unsafe-perm
RUN npm run build

RUN python manage.py collectstatic --noinput

COPY run-server.sh ./
RUN chmod +x run-server.sh