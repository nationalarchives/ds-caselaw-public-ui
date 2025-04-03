FROM mcr.microsoft.com/playwright/python:v1.51.0-noble@sha256:885e4d785085ec83d4dbfcd36c0870e076d926fc76bd52c7e424545782e98e73

WORKDIR /app

RUN pip install pytest-playwright axe-playwright-python
COPY . .

EXPOSE 9222

CMD ["tail", "-f", "/dev/null"]
