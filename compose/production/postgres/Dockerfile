FROM postgres:15.15@sha256:5f07e69ced9ee30ec814cd12c555694276bb1d520e971205f39a833362748a3c

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
