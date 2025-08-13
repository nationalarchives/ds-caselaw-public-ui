FROM postgres:15.13@sha256:ba435bcc234b52ba5f2d08d9fd6cb12e5b4e93be828be61fbae167feb2337c3d

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
