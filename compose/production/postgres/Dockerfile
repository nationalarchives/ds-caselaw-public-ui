FROM postgres:15.16@sha256:dafc4d8e8369da730a5ee9a320a0f0b3c6aa516f41244689c4493a27dc84472d

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
