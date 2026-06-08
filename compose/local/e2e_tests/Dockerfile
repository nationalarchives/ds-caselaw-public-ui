FROM mcr.microsoft.com/playwright/python:v1.60.0-noble@sha256:abf13b369f8829eb45e29df38d6c5221f7e7521649cb5d2de7989c82bdb574ad
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9222

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD test -f /proc/self/status || exit 1

USER root

CMD ["tail", "-f", "/dev/null"]
