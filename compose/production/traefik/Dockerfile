FROM traefik:v3.6.8@sha256:90099f8948c828ecf0ababd711a4359a2443eba12261c1df2f548a3b1d815938
RUN mkdir -p /etc/traefik/acme \
  && touch /etc/traefik/acme/acme.json \
  && chmod 600 /etc/traefik/acme/acme.json
COPY ./compose/production/traefik/traefik.yml /etc/traefik
