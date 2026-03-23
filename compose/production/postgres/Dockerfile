FROM postgres:15.16@sha256:2bc89eed5490967e6b1fa5175d84cb45d65f19fbb8973c7b23450dea785b9505

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
