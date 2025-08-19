FROM postgres:15.14@sha256:bc51cf4f1fe02cce7ed2370b20128a9b00b4eb804573a77d2a0d877aaa9c82b1

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
