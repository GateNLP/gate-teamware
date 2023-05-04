# only need to do the node build once, even if we're building multi-arch
FROM --platform=$BUILDPLATFORM node:18-buster-slim as nodebuilder
COPY package.json package-lock.json /app/
COPY frontend/package.json frontend/package-lock.json /app/frontend/
WORKDIR /app
RUN npm install --unsafe-perm --only=production --no-optional
COPY frontend/ /app/frontend/
RUN npm run build


FROM python:3.9-slim-buster AS backend
ARG TARGETARCH
ENV PYTHONUNBUFFERED 1
RUN apt-get --allow-releaseinfo-change update && \
    apt-get -y install gcc libpq-dev libmagic1 postgresql-client && \
    rm -rf /var/lib/apt/lists/*
ADD https://github.com/krallin/tini/releases/download/v0.19.0/tini-$TARGETARCH /sbin/tini
RUN addgroup --gid 1001 "gate" && \
      adduser --disabled-password --gecos "GATE User,,," \
        --home /app --ingroup gate --uid 1001 gate && \
      chmod +x /sbin/tini
WORKDIR /app/
COPY requirements.txt .
USER gate:gate
ENV PATH "/app/.local/bin:$PATH"
RUN pip install -r requirements.txt
RUN pip install gunicorn~=20.1.0
COPY --chown=gate:gate run-server.sh generate-docker-env.sh manage.py migrate-integration.sh ./
COPY --chown=gate:gate examples/ ./examples/
COPY --chown=gate:gate teamware/ ./teamware/
COPY --chown=gate:gate backend/ ./backend
COPY --chown=gate:gate frontend/ ./frontend/
COPY --chown=gate:gate --from=nodebuilder /app/frontend/templates/index.html ./backend/templates/
ENTRYPOINT [ "/app/run-server.sh" ]


FROM nginx:stable-alpine as frontend
COPY nginx/health.conf.template /etc/nginx/templates/
COPY --from=nodebuilder /app/frontend/public/static /usr/share/nginx/html/static
COPY --from=nodebuilder /app/frontend/dist/static /usr/share/nginx/html/static
ENV HEALTH_PORT=8888


FROM backend as test
ENV DJANGO_SETTINGS_MODULE teamware.settings.test
WORKDIR /app/
USER root
RUN apt-get update && \
    apt-get -y install curl gnupg xvfb libgtk2.0-0 libgtk-3-0 libgbm-dev libnotify-dev libgconf-2-4 libnss3 libxss1 libasound2 libxtst6 xauth
RUN curl -sL https://deb.nodesource.com/setup_18.x  | bash -
RUN apt-get -y install nodejs
USER gate:gate
COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt
COPY --from=nodebuilder --chown=gate:gate /app/ /app/
RUN npm install --no-optional
ENTRYPOINT [ "/bin/bash" ]
