FROM postgres:15.13@sha256:b8e11f8a8b383e19589a086a78b10f9ca69a39d6c9dcdd9342a8697544e8b3a0

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
