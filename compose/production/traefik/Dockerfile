FROM traefik:v3.4.4@sha256:82d2e26705a570b6d6778879d471cb3324687e77a6fd6883745a76c04563397a
RUN mkdir -p /etc/traefik/acme \
  && touch /etc/traefik/acme/acme.json \
  && chmod 600 /etc/traefik/acme/acme.json
COPY ./compose/production/traefik/traefik.yml /etc/traefik
