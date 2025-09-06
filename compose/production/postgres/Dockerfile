FROM postgres:15.14@sha256:3100d846f032aceee37895aaef39eed48d7aedf49d203c9835f3cedee3b8c9e4

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
