FROM traefik:v3.6.5@sha256:67622638cd88dbfcfba40159bc652ecf0aea0e032f8a3c7e3134ae7c037b9910
RUN mkdir -p /etc/traefik/acme \
  && touch /etc/traefik/acme/acme.json \
  && chmod 600 /etc/traefik/acme/acme.json
COPY ./compose/production/traefik/traefik.yml /etc/traefik
