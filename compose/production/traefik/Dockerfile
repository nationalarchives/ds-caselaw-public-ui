FROM traefik:v3.6.7@sha256:140d1fe3ba042682b8c93e8d0fdff043f9d6b27654bd9e84599d7ed220cf2ec7
RUN mkdir -p /etc/traefik/acme \
  && touch /etc/traefik/acme/acme.json \
  && chmod 600 /etc/traefik/acme/acme.json
COPY ./compose/production/traefik/traefik.yml /etc/traefik
