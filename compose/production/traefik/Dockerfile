FROM traefik:v3.4.4@sha256:9b0e9d788816d722703eae57ebf8b4d52ad98e02b76f0362d5a040ef46902ef7
RUN mkdir -p /etc/traefik/acme \
  && touch /etc/traefik/acme/acme.json \
  && chmod 600 /etc/traefik/acme/acme.json
COPY ./compose/production/traefik/traefik.yml /etc/traefik
