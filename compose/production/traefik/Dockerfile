FROM traefik:v3.4.4@sha256:628f1c5c9c2bcb9ee185566f9df673ca7fcda8930d39c21473523a7687020f89
RUN mkdir -p /etc/traefik/acme \
  && touch /etc/traefik/acme/acme.json \
  && chmod 600 /etc/traefik/acme/acme.json
COPY ./compose/production/traefik/traefik.yml /etc/traefik
