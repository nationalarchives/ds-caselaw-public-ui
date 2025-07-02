FROM postgres:15.13@sha256:3156e13d976072c9083fe4c56455b8515dcf6fee23fd770e6ba4a3c6b8837337

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
