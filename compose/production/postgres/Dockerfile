FROM postgres:15.12@sha256:3f109b0171ed89a798fc0f46f7cc8c04234f5a535c83ec7c4d477779cd10882f

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
