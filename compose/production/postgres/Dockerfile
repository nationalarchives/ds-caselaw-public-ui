FROM postgres:15.15@sha256:98fe06b500b5eb29e45bf8c073eb0ca399790ce17b1d586448edc4203627d342

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
