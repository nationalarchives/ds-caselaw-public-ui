FROM postgres:15.13@sha256:0d4a6674fb33f8a5581f851386522db8cd703002be486649735c08d786c0287b

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
