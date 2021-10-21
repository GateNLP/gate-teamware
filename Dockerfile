FROM node:12-buster-slim as nodebuilder
COPY package.json package-lock.json ./
COPY frontend/ ./frontend/
RUN npm install --unsafe-perm --only=production
RUN npm run build


FROM python:3.9-slim-buster AS builder
ENV PYTHONUNBUFFERED 1
RUN apt-get --allow-releaseinfo-change update && \
    apt-get -y install gcc libpq-dev libmagic1 && \
    rm -rf /var/lib/apt/lists/*
COPY manage.py count_superusers.py ./
COPY annotation_tool/ ./annotation_tool/
COPY backend/ ./backend
COPY --from=nodebuilder frontend/static ./frontend/static
COPY --from=nodebuilder frontend/public/static ./frontend/public/static
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput


FROM python:3.9-slim-buster AS backend
RUN apt-get --allow-releaseinfo-change update && \
    apt-get -y install gcc libpq-dev libmagic1 && \
    rm -rf /var/lib/apt/lists/*
ADD https://github.com/krallin/tini/releases/download/v0.19.0/tini /sbin/tini
RUN addgroup --gid 1001 "gate" && \
      adduser --disabled-password --gecos "GATE User,,," \
        --home /app --ingroup gate --uid 1001 gate && \
      chmod +x /sbin/tini
WORKDIR /app/
COPY --chown=gate:gate run-server.sh generate-env.sh ./
COPY --chown=gate:gate manage.py count_superusers.py ./
COPY --chown=gate:gate annotation_tool/ ./annotation_tool/
COPY --chown=gate:gate backend/ ./backend
COPY --chown=gate:gate examples/ ./examples/
COPY --chown=gate:gate frontend/ ./frontend/
USER gate:gate
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn
ENTRYPOINT [ "/app/run-server.sh" ]


FROM nginx:stable-alpine as frontend
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/production.conf /etc/nginx/nginx.conf
COPY --from=builder /static /usr/share/nginx/html
COPY --from=builder /frontend/ /usr/share/nginx/html/frontend
