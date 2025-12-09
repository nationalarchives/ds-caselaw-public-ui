FROM traefik:v3.6.4@sha256:c5bd185c41ba3dbb42cf8a1b9fbdc368bdc96f90c8e598134879935f64e7a7f1
RUN mkdir -p /etc/traefik/acme \
  && touch /etc/traefik/acme/acme.json \
  && chmod 600 /etc/traefik/acme/acme.json
COPY ./compose/production/traefik/traefik.yml /etc/traefik
