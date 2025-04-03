FROM traefik:v3.3.5@sha256:104204dadedf5d1284f8ef8f97f705649ac81aa6f7a6c9abf13e2c59245b8abc
RUN mkdir -p /etc/traefik/acme \
  && touch /etc/traefik/acme/acme.json \
  && chmod 600 /etc/traefik/acme/acme.json
COPY ./compose/production/traefik/traefik.yml /etc/traefik
