FROM postgres:15.14@sha256:9541969afa16d1ac724e16d1cf3c26ddd0c5bae5dd1c230118a7f5b9c14cde1f

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
