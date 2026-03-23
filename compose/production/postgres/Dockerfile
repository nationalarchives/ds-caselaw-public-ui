FROM postgres:15.17@sha256:c635fa3e3b7421a659d34abdfd6d492f679cbe8149e261a501237b55c5a94212

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
