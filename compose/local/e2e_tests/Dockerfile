FROM mcr.microsoft.com/playwright/python:v1.65.2-noble@sha256:cbd0a36dc6f6b8e8bb23703cf6cbe19ebe29e5a1ba43271a11a6c8e53c8b65d0
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9222

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD test -f /proc/self/status || exit 1

USER root

CMD ["tail", "-f", "/dev/null"]
