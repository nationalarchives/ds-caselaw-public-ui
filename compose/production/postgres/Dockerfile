FROM postgres:15.14@sha256:7927ca2ca15f9107cd2ee2004fcad3054674776a4009a63fc061cc58d0210c26

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
