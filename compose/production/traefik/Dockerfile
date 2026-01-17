FROM traefik:v3.6.7@sha256:2c5e029ee3638d3788b4ca7c8ef454baa8f924b91b190b3fd2742bee721ebeea
RUN mkdir -p /etc/traefik/acme \
  && touch /etc/traefik/acme/acme.json \
  && chmod 600 /etc/traefik/acme/acme.json
COPY ./compose/production/traefik/traefik.yml /etc/traefik
