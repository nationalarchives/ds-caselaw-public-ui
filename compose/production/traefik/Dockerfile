FROM traefik:v3.3.6@sha256:83f3c843133530e4aa45e6ddc415488583a8a01c88adc5022d415c6e97ceeaae
RUN mkdir -p /etc/traefik/acme \
  && touch /etc/traefik/acme/acme.json \
  && chmod 600 /etc/traefik/acme/acme.json
COPY ./compose/production/traefik/traefik.yml /etc/traefik
