FROM python:3.10.12-alpine

WORKDIR /app

USER root

RUN apk add --no-cache libpq postgresql-dev build-base

RUN python -m pip install --upgrade pip

COPY . .

RUN pip install --no-cache-dir -r requirements.txt


CMD ["python", "main.py"]