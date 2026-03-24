FROM mcr.microsoft.com/playwright/python:v1.57.0-noble@sha256:3de745b23fc4b33fccbcb3f592ee52dd5c80ce79f19f839c825ce23364e403c1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9222

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD test -f /proc/self/status || exit 1

USER root

CMD ["tail", "-f", "/dev/null"]
