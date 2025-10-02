FROM postgres:15.14@sha256:c189d272e4fcdd1ac419adee675d30be3d389c22ee770d593f15819d22a68a0d

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
