FROM traefik:v3.6.1@sha256:fd5932c796f7e2db9fd6bff485ef693d53797f0ee8ad03dc68aa424ea6f21958
RUN mkdir -p /etc/traefik/acme \
  && touch /etc/traefik/acme/acme.json \
  && chmod 600 /etc/traefik/acme/acme.json
COPY ./compose/production/traefik/traefik.yml /etc/traefik
