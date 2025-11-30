import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# -----------------------------
# Helper Fake Response
# -----------------------------
class FakeResp:
    def __init__(self, url, payload):
        self.status_code = 200
        self.url = url
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


def make_fake_get(mapping):
    """
    mapping = {
        "current.json": {"current": {"fake": True}},
        "forecast.json": {"forecast": {"fake": True}},
    }
    """
    def fake_get(url, params=None, timeout=None):
        endpoint = url.split("/")[-1]
        return FakeResp(url, mapping.get(endpoint, {"ok": True}))
    return fake_get


def disable_cache():
    """Disable Redis cache in your project during tests."""
    try:
        from app.utils import cache as cache_module
        cache_module._cache._client = None
    except Exception:
        pass


# -----------------------------
# TEST — HEALTH CHECK
# -----------------------------
def test_health():
    disable_cache()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


# -----------------------------
# TEST — CURRENT WEATHER
# -----------------------------
def test_current(monkeypatch):
    disable_cache()
    mapping = {
        "current.json": {"current": {"fake": True}}
    }

    monkeypatch.setattr(
        "app.services.weather_service.session.get",
        make_fake_get(mapping)
    )

    resp = client.get("/weather/current?location=Delhi")
    assert resp.status_code == 200
    data = resp.json()
    assert data["api"] == "current"
    assert data["data"]["current"]["fake"] is True


# -----------------------------
# TEST — FORECAST
# -----------------------------
def test_forecast(monkeypatch):
    disable_cache()
    mapping = {
        "forecast.json": {"forecast": {"fake": True}}
    }

    monkeypatch.setattr(
        "app.services.weather_service.session.get",
        make_fake_get(mapping)
    )

    resp = client.get("/weather/forecast?q=Delhi&days=3")
    assert resp.status_code == 200
    data = resp.json()
    assert data["api"] == "forecast"
    assert data["data"]["forecast"]["fake"] is True


# -----------------------------
# TEST — HISTORY
# -----------------------------
def test_history(monkeypatch):
    disable_cache()
    mapping = {"history.json": {"history": {"fake": True}}}

    monkeypatch.setattr(
        "app.services.weather_service.session.get",
        make_fake_get(mapping)
    )

    resp = client.get("/weather/history?q=Delhi&dt=2025-11-01")
    assert resp.status_code == 200
    data = resp.json()
    assert data["api"] == "history"
    assert data["data"]["history"]["fake"] is True


# -----------------------------
# TEST — MARINE
# -----------------------------
def test_marine_q(monkeypatch):
    disable_cache()
    mapping = {"marine.json": {"marine": {"fake": True}}}

    monkeypatch.setattr(
        "app.services.weather_service.session.get",
        make_fake_get(mapping)
    )

    resp = client.get("/weather/marine?q=BayArea")
    assert resp.status_code == 200
    data = resp.json()
    assert data["api"] == "marine"
    assert data["data"]["marine"]["fake"] is True


def test_marine_latlon(monkeypatch):
    disable_cache()
    mapping = {"marine.json": {"marine": {"fake": True}}}

    monkeypatch.setattr(
        "app.services.weather_service.session.get",
        make_fake_get(mapping)
    )

    resp = client.get("/weather/marine?lat=12.3&lon=45.6")
    assert resp.status_code == 200
    data = resp.json()
    assert data["api"] == "marine"
    assert data["data"]["marine"]["fake"] is True


# -----------------------------
# TEST — SEARCH
# -----------------------------
def test_search(monkeypatch):
    disable_cache()
    mapping = {"search.json": [{"name": "Delhi"}]}

    monkeypatch.setattr(
        "app.services.weather_service.session.get",
        make_fake_get(mapping)
    )

    resp = client.get("/weather/search?q=Delhi")
    assert resp.status_code == 200
    data = resp.json()
    assert data["data"][0]["name"] == "Delhi"


# -----------------------------
# TEST — IP LOOKUP
# -----------------------------
def test_ip_lookup(monkeypatch):
    disable_cache()
    mapping = {"ip.json": {"ip": {"result": True}}}

    monkeypatch.setattr(
        "app.services.weather_service.session.get",
        make_fake_get(mapping)
    )

    resp = client.get("/weather/ip?ip=8.8.8.8")
    assert resp.status_code == 200
    data = resp.json()
    assert data["api"] == "ip"


# -----------------------------
# TEST — TIMEZONE
# -----------------------------
def test_timezone(monkeypatch):
    disable_cache()
    mapping = {"timezone.json": {"timezone": {"fake": True}}}

    monkeypatch.setattr(
        "app.services.weather_service.session.get",
        make_fake_get(mapping)
    )

    resp = client.get("/weather/timezone?q=Delhi")
    assert resp.status_code == 200
    data = resp.json()
    assert data["api"] == "timezone"


# -----------------------------
# TEST — ASTRONOMY
# -----------------------------
def test_astronomy(monkeypatch):
    disable_cache()
    mapping = {"astronomy.json": {"astronomy": {"fake": True}}}

    monkeypatch.setattr(
        "app.services.weather_service.session.get",
        make_fake_get(mapping)
    )

    resp = client.get("/weather/astronomy?q=Delhi&dt=2025-11-30")
    assert resp.status_code == 200
    data = resp.json()
    assert data["api"] == "astronomy"


# -----------------------------
# TEST — FUTURE
# -----------------------------
def test_future(monkeypatch):
    disable_cache()
    mapping = {"future.json": {"future": {"fake": True}}}

    monkeypatch.setattr(
        "app.services.weather_service.session.get",
        make_fake_get(mapping)
    )

    resp = client.get("/weather/future?q=Delhi&days=7")
    assert resp.status_code == 200
    data = resp.json()
    assert data["api"] == "future"


# -----------------------------
# TEST — GENERIC API
# -----------------------------
def test_generic_api(monkeypatch):
    disable_cache()
    mapping = {"current.json": {"current": {"fake": True}}}

    monkeypatch.setattr(
        "app.services.weather_service.session.get",
        make_fake_get(mapping)
    )

    resp = client.get("/weather/api/current?q=Delhi")
    assert resp.status_code == 200
    data = resp.json()
    assert data["api"] == "current"
    assert data["data"]["current"]["fake"] is True
