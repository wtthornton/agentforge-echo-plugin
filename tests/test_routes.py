from fastapi import FastAPI
from fastapi.testclient import TestClient

from agentforge_echo.plugin import register


def _build_app() -> FastAPI:
    app = FastAPI()
    register(app)
    return app


def test_status():
    client = TestClient(_build_app())
    resp = client.get("/api/echo/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["plugin"] == "echo"
    assert data["version"] == "1.0.0"


def test_echo_reverses():
    client = TestClient(_build_app())
    resp = client.post("/api/echo/echo", json={"msg": "hello"})
    assert resp.status_code == 200
    assert resp.json() == {"echoed": "hello", "reversed": "olleh"}


def test_echo_without_bus_still_works():
    # app.state.topic_bus is None → route skips emit, still returns 200
    client = TestClient(_build_app())
    resp = client.post("/api/echo/echo", json={"msg": "x"})
    assert resp.status_code == 200
