FROM postgres:15.15@sha256:a7711af921c380de0fda7c48a61fab5ac4def145fd9fc00ccea7355fd6270bb4

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
