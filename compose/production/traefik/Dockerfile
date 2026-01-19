FROM traefik:v3.6.7@sha256:ebe7d3fc715e28f033cea8265e9105b9d64705867f5b916e2d9ed0b62c530192
RUN mkdir -p /etc/traefik/acme \
  && touch /etc/traefik/acme/acme.json \
  && chmod 600 /etc/traefik/acme/acme.json
COPY ./compose/production/traefik/traefik.yml /etc/traefik
