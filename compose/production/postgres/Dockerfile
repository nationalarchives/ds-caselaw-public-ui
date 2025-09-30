FROM postgres:15.14@sha256:2a75754bd71703145985429c5e3fd1fa4e4699940610c058748549cde66a0628

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
