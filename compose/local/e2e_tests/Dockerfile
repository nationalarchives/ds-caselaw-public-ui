FROM python:3.13

WORKDIR /app

RUN pip install pytest pytest-playwright axe-playwright-python
RUN playwright install-deps
RUN playwright install
COPY . .

EXPOSE 9222

CMD ["true"]
