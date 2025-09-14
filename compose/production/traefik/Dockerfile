FROM traefik:v3.5.2@sha256:f0abbbd11ced29754d4d188c29e9320b613481ec162b6ea5d3a8b6bdd8e5fa54
RUN mkdir -p /etc/traefik/acme \
  && touch /etc/traefik/acme/acme.json \
  && chmod 600 /etc/traefik/acme/acme.json
COPY ./compose/production/traefik/traefik.yml /etc/traefik
