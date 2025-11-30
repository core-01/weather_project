from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_forecast(monkeypatch):
    # Fake response object for session.get
    class FakeResp:
        def __init__(self):
            self.status_code = 200
            self.url = "https://api.test/forecast.json?q=Delhi&days=3"

        def raise_for_status(self):
            return None

        def json(self):
            return {"forecast": {"fake": True}}

    def fake_get(url, params=None, timeout=None):
        return FakeResp()

    monkeypatch.setattr('app.services.weather_service.session.get', fake_get)
    # Ensure cache is disabled for test (no REDIS_URL)
    try:
        from app.utils.cache import _cache
        _cache._client = None
    except Exception:
        pass

    resp = client.get("/weather/forecast?q=Delhi&days=3")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "success"
    assert body["api"] == "forecast"
    assert body["data"]["forecast"]["fake"] is True
