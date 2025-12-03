FROM postgres:15.15@sha256:24d6c206bba8c0440bceb24a8d4bf642f60bf7aea94887051ea5761d29c22323

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
