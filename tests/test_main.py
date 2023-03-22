import datetime
from _decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from db.base import db, PostgresDatabase
from db.schemas import StatisticsAggregatedResponseSchema
from main import app

FIRST_DAY = datetime.date(day=1, month=1, year=2022)


async def override_get_db():
    db = PostgresDatabase()
    db.setup()
    async_gen_session = db()
    s = await anext(async_gen_session)
    yield s
    try:
        await s.commit()
    except Exception as e:
        print(e)


app.dependency_overrides[db] = override_get_db


@pytest.fixture()
def test_db():
    db.setup()


client = TestClient(app)


def make_request(url: str) -> tuple[StatisticsAggregatedResponseSchema, int]:
    r = client.get(url)
    return StatisticsAggregatedResponseSchema(**r.json()), r.status_code


def test_read_item():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"message": "Hello from statistics service."}


def test_len_statistics():
    j, s = make_request("/statistics/")
    assert s == 200
    assert len(j.statistics) == 100


def test_len_statistics_sort_from_date():
    j, s = make_request(f"/statistics/?from={FIRST_DAY + datetime.timedelta(days=51)}")
    assert s == 200
    assert len(j.statistics) == 50
    assert j.total_clicks == 4937
    assert j.average_cpm == Decimal("1000.17")
    assert j.total_views == 4937


def test_len_statistics_sort_from_to_date():
    d1 = FIRST_DAY + datetime.timedelta(days=51)
    d2 = FIRST_DAY + datetime.timedelta(days=80)
    j, s = make_request(f"/statistics/?from={d1}&to={d2}")
    assert s == 200
    assert len(j.statistics) == 30
    assert j.total_clicks == 3000
    assert j.average_cpm == 1000
    assert j.total_views == 3000
    assert j.total_cost == 3000
    dates = [s.date for s in j.statistics]
    assert d1 == dates[0]
    assert d2 == dates[-1]


def test_sort_by_cost_asc():
    j, s = make_request(f"/statistics/?order_by=cost&order=asc")
    assert s == 200
    assert j.statistics[0].cost == Decimal("37.84")


def test_sort_by_cost_desc():
    j, s = make_request(f"/statistics/?order_by=cost&order=desc")
    assert s == 200
    assert j.statistics[-1].cost == Decimal("37.84")


def test_sort_by_clicks_asc():
    j, s = make_request(f"/statistics/?order_by=cost&order=asc")
    assert s == 200
    assert j.statistics[0].clicks == 37


def test_sort_by_clicks_desc():
    j, s = make_request(f"/statistics/?order_by=cost&order=desc")
    assert s == 200
    assert j.statistics[-1].clicks == 37


def test_sort_by_views_asc():
    j, s = make_request(f"/statistics/?order_by=views&order=asc")
    assert s == 200
    assert j.statistics[0].views == 37


def test_sort_by_views_desc():
    j, s = make_request(f"/statistics/?order_by=views&order=desc")
    assert s == 200
    assert j.statistics[-1].views == 37


def test_sort_by_views_asc_with_date():
    d1 = FIRST_DAY + datetime.timedelta(days=99)
    d2 = FIRST_DAY + datetime.timedelta(days=101)
    j, s = make_request(f"/statistics/?from={d1}&to={d2}&?order_by=views&order=asc")
    assert s == 200
    assert len(j.statistics) == 2
    assert j.statistics[0].views == 100
    assert j.statistics[-1].views == 37


def test_sort_by_views_desc_with_date():
    d1 = FIRST_DAY + datetime.timedelta(days=99)
    d2 = FIRST_DAY + datetime.timedelta(days=101)
    j, s = make_request(f"/statistics/?from={d1}&to={d2}&?order_by=views&order=desc")
    assert s == 200
    assert len(j.statistics) == 2
    assert j.statistics[0].views == 37
    assert j.statistics[-1].views == 100


def test_204():
    d1 = FIRST_DAY + datetime.timedelta(days=101)
    r = client.get(f"/statistics/?from={d1}")
    assert r.status_code == 204


def test_reset():
    j, _ = make_request("/statistics")
    assert len(j.statistics) == 100
    r = client.put("/statistics")
    assert r.status_code == 200
    r = client.get("/statistics")
    assert r.status_code == 204
    assert r.json() == {}


def test_post():
    j = {"date": "2020-01-18", "views": 138, "clicks": 26, "cost": 1234.56}
    r = client.post("/statistics/", json=j)
    assert r.status_code == 200
    assert r.json() == j


def test_post_422_unique_date():
    j = {"date": "2020-01-18", "views": 138, "clicks": 26, "cost": 1234.56}
    r = client.post("/statistics/", json=j)
    assert r.status_code == 422


def test_post_date_is_greater():
    j = {"date": "2028-01-18", "views": 138, "clicks": 26, "cost": 1234.56}
    r = client.post("/statistics/", json=j)
    assert r.status_code == 422


def test_post_null():
    j = {"date": "2019-01-18", "views": None, "clicks": None, "cost": None}
    r = client.post("/statistics/", json=j)
    assert r.status_code == 200
    assert r.json()["date"] == j["date"]
    assert r.json()["clicks"] == 0
    assert r.json()["views"] == 0
    assert r.json()["cost"] == 0


def test_post_with_fp():
    r = client.post("/statistics", json={
        "date": "2012-03-22",
        "views": 1.22,
        "clicks": 1,
        "cost": 1.22
    })
    assert r.status_code == 422
    assert r.json()["detail"][0]["msg"] == "Not acceptable, views can't be a number with a floating point."
    r = client.post("/statistics", json={
        "date": "2012-03-22",
        "views": 1,
        "clicks": 1.22,
        "cost": 1.22
    })
    assert r.status_code == 422
    assert r.json()["detail"][0]["msg"] == "Not acceptable, clicks can't be a number with a floating point."
