FROM postgres:15.14@sha256:08155957f670000953ad9bf7f654a13bb0d4fb01b8f1cc83736f2fd18601aab4

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
