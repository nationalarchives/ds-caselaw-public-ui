FROM postgres:15.12@sha256:3e7f69031397fdae46965e9c300fec7338f8db2acd345d28f35da39a4337ac86

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
