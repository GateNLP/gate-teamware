FROM continuumio/miniconda3:latest

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE annotation_tool.settings.staging

SHELL ["/bin/bash", "-c"]

RUN apt-get --allow-releaseinfo-change update && \
    apt-get -y install gcc apache2-dev libpq-dev libmagic1 && \
    rm -rf /var/lib/apt/lists/*

ADD https://github.com/krallin/tini/releases/download/v0.19.0/tini /sbin/tini
RUN chmod +x /sbin/tini

RUN mkdir /app
ADD . /app/
WORKDIR /app
COPY environment.yml .
RUN chmod u+x environment.yml
RUN conda env create --name annotation-tool --file environment.yml
RUN conda install --name annotation-tool gunicorn

COPY package.json package-lock.json ./
COPY frontend/package.json frontend/package-lock.json frontend/

# # Make RUN commands use the conda environment:
# SHELL ["conda", "run", "-n", "annotation-tool", "/bin/bash", "-c"]
RUN source activate annotation-tool && \
    npm install --unsafe-perm
RUN source activate annotation-tool && \
    npm run build

# collectstatic doesn't need *valid* secret settings, but the command will complain if the settings don't exist at all
RUN echo "SECRET_KEY='dummy'" > /app/annotation_tool/settings/secret.py && \
    source activate annotation-tool && \
    python manage.py collectstatic --noinput && \
    rm /app/annotation_tool/settings/secret.py

EXPOSE 8000

COPY run-server.sh ./
RUN chmod +x run-server.sh