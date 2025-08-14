FROM postgres:15.13@sha256:15d29ec7af31e0f60c2394ed5e3b4d45b6b8d78ffc6faf994e9796c1415b8785

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
