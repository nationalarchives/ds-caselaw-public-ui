FROM traefik:v3.4.1@sha256:cd40ab7bc1f047731d5b22595203812343efcb6538014c4e93221cfc3a77217a
RUN mkdir -p /etc/traefik/acme \
  && touch /etc/traefik/acme/acme.json \
  && chmod 600 /etc/traefik/acme/acme.json
COPY ./compose/production/traefik/traefik.yml /etc/traefik
