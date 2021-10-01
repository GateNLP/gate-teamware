FROM continuumio/miniconda3:latest

ENV PYTHONUNBUFFERED 1

RUN apt-get --allow-releaseinfo-change update && \
    apt-get -y install gcc libpq-dev libmagic1 && \
    rm -rf /var/lib/apt/lists/*

ADD https://github.com/krallin/tini/releases/download/v0.19.0/tini /sbin/tini
RUN addgroup --gid 1001 "gate" && \
      adduser --disabled-password --gecos "GATE User,,," \
        --home /app --ingroup gate --uid 1001 gate && \
      chmod +x /sbin/tini

COPY --chown=gate:gate environment.yml /app/
WORKDIR /app
RUN chown --recursive gate:gate /opt/conda/
USER gate:gate
RUN conda env create --name annotation-tool --file environment.yml
RUN conda install --name annotation-tool gunicorn

COPY --chown=gate:gate package.json package-lock.json /app/
COPY --chown=gate:gate frontend/package.json frontend/package-lock.json /app/frontend/

SHELL ["conda", "run", "-n", "annotation-tool", "/bin/bash", "-c"]

RUN npm install --unsafe-perm --only=production

COPY --chown=gate:gate manage.py /app/
COPY --chown=gate:gate examples/ /app/examples/
COPY --chown=gate:gate annotation_tool/ /app/annotation_tool/
COPY --chown=gate:gate backend/ /app/backend
COPY --chown=gate:gate frontend/ /app/frontend/
RUN npm run build
RUN python manage.py collectstatic --noinput

COPY --chown=gate:gate run-server.sh generate-env.sh /app/

ENTRYPOINT [ "/app/run-server.sh" ]
