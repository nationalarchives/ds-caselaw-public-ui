FROM postgres:15.12@sha256:fe45ed1a824b81c0c9c605890963b67501758ca8c946db89089c85ce0f88e974

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
