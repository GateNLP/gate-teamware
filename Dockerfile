FROM node:12-buster-slim as nodebuilder
COPY package.json package-lock.json ./
COPY frontend/package.json frontend/package-lock.json ./frontend/
RUN npm install --unsafe-perm --only=production
COPY frontend/ ./frontend/
RUN npm run build


FROM python:3.9-slim-buster AS backend
ENV PYTHONUNBUFFERED 1
RUN apt-get --allow-releaseinfo-change update && \
    apt-get -y install gcc libpq-dev libmagic1 && \
    rm -rf /var/lib/apt/lists/*
ADD https://github.com/krallin/tini/releases/download/v0.19.0/tini /sbin/tini
RUN addgroup --gid 1001 "gate" && \
      adduser --disabled-password --gecos "GATE User,,," \
        --home /app --ingroup gate --uid 1001 gate && \
      chmod +x /sbin/tini
WORKDIR /app/
COPY requirements.txt .
USER gate:gate
RUN pip install -r requirements.txt
RUN pip install gunicorn~=20.1.0
COPY --chown=gate:gate run-server.sh generate-env.sh count_superusers.py manage.py ./
COPY --chown=gate:gate examples/ ./examples/
COPY --chown=gate:gate annotation_tool/ ./annotation_tool/
COPY --chown=gate:gate backend/ ./backend
COPY --chown=gate:gate frontend/ ./frontend/
COPY --chown=gate:gate --from=nodebuilder /frontend/templates/base-vue.html ./backend/templates/
ENTRYPOINT [ "/app/run-server.sh" ]


FROM nginx:stable-alpine as frontend
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/production.conf /etc/nginx/nginx.conf
COPY --from=nodebuilder /frontend/static /usr/share/nginx/html
COPY --from=nodebuilder /frontend/public/static /usr/share/nginx/html
