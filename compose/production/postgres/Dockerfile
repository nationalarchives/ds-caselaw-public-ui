FROM postgres:15.14@sha256:31e60cbedcb3baa718f758db049e9111494f5ef8e9c18f52a95db746a68ef049

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
