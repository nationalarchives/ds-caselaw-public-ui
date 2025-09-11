FROM postgres:15.14@sha256:1cd9dd548427751dc0fabb24a3bdf96a6dd08c0025a167ecbb5c14bec21ff94c

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
