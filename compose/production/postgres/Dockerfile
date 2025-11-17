FROM postgres:15.15@sha256:c23f5a12ca4e848f8fcd85a74f348888a89e04916a98726b00697af36ec0a700

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
