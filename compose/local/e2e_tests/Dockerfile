FROM mcr.microsoft.com/playwright/python:v1.54.0-noble@sha256:9e85bdc9c6980dc230c17f3548acb8d2d73b2cb2d5f6e34e706e18464559ef63

WORKDIR /app

RUN pip install pytest-playwright axe-playwright-python pillow numpy scikit-image
COPY . .

EXPOSE 9222

CMD ["tail", "-f", "/dev/null"]
