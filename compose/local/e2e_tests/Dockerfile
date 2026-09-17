FROM mcr.microsoft.com/playwright/python:v1.63.0-noble@sha256:96b39581c89131729a7ecb8d532314af54c7f9bcc7a61fe15c7a9e77602acf59
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9222

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD test -f /proc/self/status || exit 1

USER root

CMD ["tail", "-f", "/dev/null"]
