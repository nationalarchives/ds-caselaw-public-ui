ARG PYTHON_VERSION=3.9-slim-bullseye



# define an alias for the specfic python version used in this file.
FROM python:${PYTHON_VERSION} as python

# Python build stage
FROM python as python-build-stage

ARG BUILD_ENVIRONMENT=production

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # WeasyPrint dependencies \
  weasyprint \
  python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0

# Requirements are installed here to ensure they will be cached.
COPY pyproject.toml .
COPY poetry.lock .

# Python 'run' stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=production
ARG APP_HOME=/app
ARG USER=django
ARG GROUP=django

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

USER ${USER}
WORKDIR ${APP_HOME}

# Create group and add user to it
RUN addgroup --system ${GROUP} \
    && adduser --system --ingroup ${GROUP} ${USER}

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg2 dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  curl \
  # WeasyPrint dependencies \
  weasyprint \
  python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0 \
  # node install
  nodejs npm \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*
RUN npm i -g sass

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
# COPY --from=python-build-stage /usr/src/app/  /wheels/

RUN poetry install --with prod

# copy over npm dependencies with ownership and install
COPY --chown=${USER}:${GROUP} package-lock.json package-lock.json
COPY --chown=${USER}:${GROUP} package.json package.json
RUN npm ci

# copy over production docker entrpoint script with ownership and make executable
COPY --chown=${USER}:${GROUP} ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

# copy over production docker start script with ownership and make executable
COPY --chown=${USER}:${GROUP} ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# copy application code with ownership to WORKDIR
COPY --chown=${USER}:${GROUP} . ${APP_HOME}

# make user and group the owner of the WORKDIR directory as well.
RUN chown ${USER}:${GROUP} ${APP_HOME}

ENTRYPOINT ["/entrypoint"]

EXPOSE 5000

CMD /start
