FROM nginx:stable-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY production.conf /etc/nginx/nginx.conf
COPY --from=backend:latest /app/static /usr/share/nginx/html
COPY --from=backend:latest /app/frontend/ /usr/share/nginx/html/frontend
