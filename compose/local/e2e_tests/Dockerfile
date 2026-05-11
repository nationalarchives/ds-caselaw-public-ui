FROM mcr.microsoft.com/playwright/python:v1.59.0-noble@sha256:01671e89f7b85dcdc35bebdc96b5fee2a5fd7f10d607fc9ae00bf094f5e94f26
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9222

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD test -f /proc/self/status || exit 1

USER root

CMD ["tail", "-f", "/dev/null"]
