FROM traefik:v3.4.3@sha256:f3de2b96ec6b1cc987619c4d1d65d7e8140862eb0bbfc5f0e2e563691e8787d8
RUN mkdir -p /etc/traefik/acme \
  && touch /etc/traefik/acme/acme.json \
  && chmod 600 /etc/traefik/acme/acme.json
COPY ./compose/production/traefik/traefik.yml /etc/traefik
