FROM postgres:15.14@sha256:5f64cfd881133fd1802eb12abaf6e5e54cd628d087789a00855262fffe8f26de

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
