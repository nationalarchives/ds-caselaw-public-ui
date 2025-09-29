FROM postgres:18.0@sha256:1d288494853e244e7a78d87b3526e650e5221c622f9768ecac9313d0874a9c39

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
