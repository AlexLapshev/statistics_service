FROM python:3.10-slim

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY . .
WORKDIR .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000