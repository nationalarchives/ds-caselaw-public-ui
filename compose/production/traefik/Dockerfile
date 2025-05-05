FROM traefik:v3.3.7@sha256:2cd5cc75530c8d07ae0587c743d23eb30cae2436d07017a5ff78498b1a43d09f
RUN mkdir -p /etc/traefik/acme \
  && touch /etc/traefik/acme/acme.json \
  && chmod 600 /etc/traefik/acme/acme.json
COPY ./compose/production/traefik/traefik.yml /etc/traefik
