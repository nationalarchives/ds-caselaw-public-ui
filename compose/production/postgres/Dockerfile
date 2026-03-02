FROM postgres:15.17@sha256:07b491ffc6f20c74e5a734119c06f1f321ec0c710ca37f137d7c70ed5b7adae9

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
