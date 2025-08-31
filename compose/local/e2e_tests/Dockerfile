FROM mcr.microsoft.com/playwright/python:v1.55.0-noble@sha256:640d578aae63cfb632461d1b0aecb01414e4e020864ac3dd45a868dc0eff3078

WORKDIR /app

RUN pip install pytest-playwright axe-playwright-python pillow numpy scikit-image
COPY . .

EXPOSE 9222

CMD ["tail", "-f", "/dev/null"]
