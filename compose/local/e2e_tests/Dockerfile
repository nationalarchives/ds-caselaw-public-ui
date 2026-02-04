FROM mcr.microsoft.com/playwright/python:v1.58.0-noble@sha256:678457c4c323b981d8b4befc57b95366bb1bb6aa30057b1269f6b171e8d9975a

WORKDIR /app

RUN pip install playwright==1.54.0 && \
    playwright install --with-deps

RUN pip install --no-cache-dir pytest-playwright==0.7.2 axe-playwright-python==0.1.7 pillow==12.1.0 numpy==2.4.2 scikit-image==0.26.0
COPY . .

EXPOSE 9222

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD test -f /proc/self/status || exit 1

USER root

CMD ["tail", "-f", "/dev/null"]
