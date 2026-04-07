FROM postgres:15.17@sha256:31224c60946ea75ee9522e0f4d02eb202e74754adea4294fdefe9f93c875b657

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
