FROM mcr.microsoft.com/playwright/python:v1.53.0-noble@sha256:648e2d7cb4136587116ba42bc4b1f7d23a6776f3237d5c27995f338c1e57f73f

WORKDIR /app

RUN pip install pytest-playwright axe-playwright-python pillow numpy scikit-image
COPY . .

EXPOSE 9222

CMD ["tail", "-f", "/dev/null"]
