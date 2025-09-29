FROM traefik:v3.5.3@sha256:84eb6c0e67c99fa026bf1bf4b0afd9ad44350d375b4ebc5049c5f70543a729d6
RUN mkdir -p /etc/traefik/acme \
  && touch /etc/traefik/acme/acme.json \
  && chmod 600 /etc/traefik/acme/acme.json
COPY ./compose/production/traefik/traefik.yml /etc/traefik
