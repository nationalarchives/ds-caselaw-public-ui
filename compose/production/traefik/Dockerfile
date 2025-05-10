FROM traefik:v3.4.0@sha256:4cf907247939b5d20bf4eff73abd21cb413c339600dde76dbc94a874b2578a27
RUN mkdir -p /etc/traefik/acme \
  && touch /etc/traefik/acme/acme.json \
  && chmod 600 /etc/traefik/acme/acme.json
COPY ./compose/production/traefik/traefik.yml /etc/traefik
