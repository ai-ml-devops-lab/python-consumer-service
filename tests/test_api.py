from __future__ import annotations

from fastapi.testclient import TestClient

from consumer_service.api import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "implementation" in data
    assert "uptime_seconds" in data


def test_score_cors_preflight():
    response = client.options(
        "/score",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_ready_and_version():
    r = client.get("/ready")
    assert r.status_code == 200
    assert r.json()["status"] == "ready"

    v = client.get("/version")
    assert v.status_code == 200
    assert v.json()["service"] == "Python Consumer Service"


def test_score_success():
    response = client.post("/score", json={"values": [1, 2, 3, 4], "window": 2})
    assert response.status_code == 200
    assert response.json()["moving_average"] == [1.5, 2.5, 3.5]


def test_score_invalid_window():
    response = client.post("/score", json={"values": [1, 2, 3], "window": 0})
    assert response.status_code == 422


def test_score_empty_values():
    response = client.post("/score", json={"values": [], "window": 2})
    assert response.status_code == 422
