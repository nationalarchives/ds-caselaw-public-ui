ARG PYTHON_VERSION=3.14-slim-bookworm@sha256:55e465cb7e50cd1d7217fcb5386aa87d0356ca2cd790872142ef68d9ef6812b4

# define an alias for the specfic python version used in this file.
FROM python:${PYTHON_VERSION} AS python

# Python build stage (shared by both local and production)
FROM python AS python-build-stage

ARG BUILD_ENVIRONMENT=production

# Install apt packages for building
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # WeasyPrint dependencies
  weasyprint \
  python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0 \
  && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
COPY ./requirements .

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip wheel --wheel-dir /usr/src/app/wheels  \
  -r ${BUILD_ENVIRONMENT}.txt


# Shared runtime stage (common dependencies for both local and production)
FROM python AS python-runtime-stage

ARG APP_HOME=/app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR ${APP_HOME}

# Install runtime system dependencies (shared by both local and production)
RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg2 dependencies
  libpq-dev \
  # WeasyPrint dependencies
  weasyprint \
  python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0 \
  && rm -rf /var/lib/apt/lists/*

# Copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

# Install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/


# Local development stage
FROM python-runtime-stage AS python-local-stage

ARG BUILD_ENVIRONMENT=local
ENV BUILD_ENV=${BUILD_ENVIRONMENT}

# Install additional development and debugging tools
RUN apt-get update && apt-get install --no-install-recommends -y \
  fonts-liberation \
  lldb \
  procps \
  libcap2-bin \
  && rm -rf /var/lib/apt/lists/*

# Copy application code to WORKDIR
COPY . ${APP_HOME}

# Run as root for local development (no permission issues with volume mounts)
# Do nothing forever (use 'docker compose exec' to run commands)
CMD ["tail", "-f", "/dev/null"]


# Production stage
FROM python-runtime-stage AS python-production-stage

ARG BUILD_ENVIRONMENT=production
ENV BUILD_ENV=${BUILD_ENVIRONMENT}

# Create non-root user for production
RUN addgroup --system django \
    && adduser --system --ingroup django --home /home/django django

# Install production-specific dependencies (curl for Node.js installation)
RUN apt-get update && apt-get install --no-install-recommends -y \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Install Node.js and clean up in one layer
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
  && apt-get install --no-install-recommends -y nodejs \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Install Node.js dependencies (as root)
COPY --chown=django:django package-lock.json package.json ./
RUN npm ci --engine-strict=true

# Copy application code (owned by django for now - will change in later PR)
COPY --chown=django:django . ${APP_HOME}

# Copy and prepare production scripts
COPY --chown=django:django ./compose/docker/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY --chown=django:django ./compose/docker/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# Create directories that need to be writable by the django user
RUN mkdir -p ${APP_HOME}/media ${APP_HOME}/logs \
  && chown -R django:django ${APP_HOME}/media ${APP_HOME}/logs

# Run as non-root user in production
USER django

ENTRYPOINT ["/entrypoint"]

EXPOSE 5000

CMD ["/start"]
