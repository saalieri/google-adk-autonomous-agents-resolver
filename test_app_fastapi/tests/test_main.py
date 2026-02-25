import os
import sys
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app


client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_crud_flow():
    # create
    r = client.post("/items", json={"name": "foo", "description": "bar"})
    assert r.status_code == 201
    item = r.json()
    assert isinstance(item.get("id"), int) and item["id"] >= 1
    assert item["name"] == "foo"
    assert "Location" in r.headers
    loc = r.headers["Location"]

    # list
    r = client.get("/items")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

    # get
    r = client.get(loc)
    assert r.status_code == 200

    # update
    r = client.put(loc, json={"name": "foo2", "description": "baz"})
    assert r.status_code == 200
    assert r.json()["name"] == "foo2"

    # delete
    r = client.delete(loc)
    assert r.status_code == 204

    # not found after delete
    r = client.get(loc)
    assert r.status_code == 404


def test_validation():
    r = client.post("/items", json={"name": ""})
    assert r.status_code == 422
