FROM python:3.12

WORKDIR /app

RUN pip install pytest pytest-playwright
RUN playwright install-deps
RUN playwright install
COPY . .

EXPOSE 9222

CMD ["true"]
