FROM postgres:15.13@sha256:2c39cacf617d2225824831e0491510ea51c0138cb4f63c4299bd73de1d942b0e

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
