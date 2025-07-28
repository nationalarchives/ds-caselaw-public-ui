FROM postgres:15.13@sha256:5ab68e212eab9cd4a16ecbf40d9449c88e1073abdca3ecc3aa5514d4a1af2ed0

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
