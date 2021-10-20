ARG FILES_FROM=backend:latest
FROM ${FILES_FROM} AS backend-image

FROM nginx:stable-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY production.conf /etc/nginx/nginx.conf
COPY --from=backend-image /app/static /usr/share/nginx/html
COPY --from=backend-image /app/frontend/ /usr/share/nginx/html/frontend
