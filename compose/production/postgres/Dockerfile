FROM postgres:15.13@sha256:e652befe0cc7d0e312828d71522aed8ed3762d6b71b6a5a823821ff06c186a20

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
