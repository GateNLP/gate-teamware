FROM continuumio/miniconda3:latest

ENV PYTHONUNBUFFERED 1

RUN apt-get --allow-releaseinfo-change update && \
    apt-get -y install gcc libpq-dev libmagic1 && \
    rm -rf /var/lib/apt/lists/*

ADD https://github.com/krallin/tini/releases/download/v0.19.0/tini /sbin/tini
RUN chmod +x /sbin/tini

COPY environment.yml /app/
WORKDIR /app
RUN conda env create --name annotation-tool --file environment.yml
RUN conda install --name annotation-tool gunicorn

COPY package.json package-lock.json /app/
COPY frontend/package.json frontend/package-lock.json /app/frontend/

SHELL ["conda", "run", "-n", "annotation-tool", "/bin/bash", "-c"]

RUN npm install --unsafe-perm --only=production

COPY manage.py /app/
COPY examples/ /app/examples/
COPY annotation_tool/ /app/annotation_tool/
COPY backend/ /app/backend
COPY frontend/ /app/frontend/
RUN npm run build
RUN python manage.py collectstatic --noinput

COPY run-server.sh generate-env.sh /app/

ENTRYPOINT [ "/app/run-server.sh" ]
