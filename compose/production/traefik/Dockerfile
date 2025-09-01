FROM traefik:v3.5.1@sha256:664bb8415fddadb71c2682b329c427d12c7d53593171665f2b7b6ff924509bc1
RUN mkdir -p /etc/traefik/acme \
  && touch /etc/traefik/acme/acme.json \
  && chmod 600 /etc/traefik/acme/acme.json
COPY ./compose/production/traefik/traefik.yml /etc/traefik
