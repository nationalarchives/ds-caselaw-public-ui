FROM postgres:15.14@sha256:424e79b81868f5fc5cf515eaeac69d288692ebcca7db86d98f91b50d4bce64bb

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
