FROM postgres:15.15@sha256:697ff70295146d53b702b07532fe68aaed7a5f10d04ff68edbeffd5fbacd15a5

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
