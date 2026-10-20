FROM mcr.microsoft.com/playwright/python:v1.64.0-noble@sha256:07c5362a4512ffca347cc5d1a888ff5e6375ff6b9314e97813effcc0fc7d5593
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9222

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD test -f /proc/self/status || exit 1

USER root

CMD ["tail", "-f", "/dev/null"]
