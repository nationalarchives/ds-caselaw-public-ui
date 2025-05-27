FROM postgres:15.13@sha256:f57a3bdbf044f0b213fdc99f35a0d21c401608bf41f063176ec00c51df9655f7

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
