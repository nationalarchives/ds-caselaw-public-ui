FROM postgres:15.17@sha256:f30e3de0ac9cc938dac627ef2231099867c694b5f949fadb924c8c977428c399

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
