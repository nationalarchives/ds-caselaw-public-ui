FROM postgres:15.12@sha256:9e9298817d19f4bd60c5028a25762b394db37dda173dd3d035a1bc155542051a

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
