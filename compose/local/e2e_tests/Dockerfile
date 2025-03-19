FROM mcr.microsoft.com/playwright/python:v1.51.0-noble

WORKDIR /app

RUN pip install pytest-playwright axe-playwright-python
COPY . .

EXPOSE 9222

CMD ["tail", "-f", "/dev/null"]
