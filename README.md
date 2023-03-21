## Installation

Create virtual environment

`python3.10 -m virtualenv venv`

Activate it

`source venv/bin/activate`

Install required packages

`pip install -r requirements.txt`

Run a database from a docker-compose file

```
docker-compose up -d 
```

Apply migrations 

```
alembic upgrade head
```

To fill the database with dummy data use 

```
python -m etc.fill_db
```


To run the app 

`python main.py`

## To run the app from docker compose

Run docker compose

```
docker-compose --profile with_api up -d 
```

## Tests

To run the tests use make file

`make test`

## Examples of CURL requests

Get statistics

```
curl --location --request GET 'http://localhost:8000/statistics'
```

```
curl --location --request GET 'http://localhost:8000/statistics/?from=2020-01-01&to=2023-01-01&order_by=clicks&order=asc'
```

Post statistics

```
curl --location --request POST 'http://localhost:8000/statistics' \
--header 'Content-Type: application/json' \
--data-raw '{
  "date": "2019-03-21",
  "views": 22,
  "clicks": 1,
  "cost": 1
}'
```

```
curl --location --request POST 'http://localhost:8000/statistics' \
--header 'Content-Type: application/json' \
--data-raw '{
  "date": "2019-03-21",
  "views": null,
  "clicks": null,
  "cost": null
}'
```

Reset statistics

```
curl --location --request PUT 'http://localhost:8000/statistics'
```
