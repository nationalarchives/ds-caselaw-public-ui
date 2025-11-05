FROM postgres:15.14@sha256:822f8795764a670160640888508b2a68ea5c4b045012c2de17e1d0447bdbdc99

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
