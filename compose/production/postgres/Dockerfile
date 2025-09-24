FROM postgres:15.14@sha256:59989294958400315a6b01e0acee42e72757d813c5434f3f0a9c5bfd5fb25219

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
