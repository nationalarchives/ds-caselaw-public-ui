FROM mcr.microsoft.com/playwright/python:v1.57.0-noble@sha256:3de745b23fc4b33fccbcb3f592ee52dd5c80ce79f19f839c825ce23364e403c1

WORKDIR /app

RUN pip install playwright==1.54.0 && \
    playwright install --with-deps

RUN pip install pytest-playwright axe-playwright-python pillow numpy scikit-image
COPY . .

EXPOSE 9222

CMD ["tail", "-f", "/dev/null"]
