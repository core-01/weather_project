from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

class FakeResp:
    def __init__(self, url, payload=None):
        self.status_code = 200
        self.url = url
        self._payload = payload or {"ok": True}
    def raise_for_status(self):
        return None
    def json(self):
        return self._payload


def make_fake_get(mapping):
    def fake_get(url, params=None, timeout=None):
        end = url.split('/')[-1] if isinstance(url, str) else 'unknown'
        payload = mapping.get(end, {"ok": True})
        return FakeResp(url, payload)
    return fake_get


def disable_cache():
    try:
        from app.utils import cache as cache_module
        cache_module._cache._client = None
    except Exception:
        pass


def test_health():
    disable_cache()
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.json().get('status') == 'ok'


def test_forecast(monkeypatch):
    disable_cache()
    mapping = {'forecast.json': {"forecast": {"fake": True}}}
    monkeypatch.setattr('app.services.weather_service.session.get', make_fake_get(mapping))
    resp = client.get('/weather/forecast?q=Delhi&days=3')
    assert resp.status_code == 200
    body = resp.json()
    assert body['status'] == 'success'
    assert body['api'] == 'forecast'
    assert body['data']['forecast']['fake'] is True


def test_history(monkeypatch):
    disable_cache()
    mapping = {'history.json': {"history": {"fake": True}}}
    monkeypatch.setattr('app.services.weather_service.session.get', make_fake_get(mapping))
    resp = client.get('/weather/history?q=Delhi&dt=2025-11-01')
    assert resp.status_code == 200
    body = resp.json()
    assert body['status'] == 'success'
    assert body['api'] == 'history'
    assert body['data']['history']['fake'] is True


def test_marine_by_q(monkeypatch):
    disable_cache()
    mapping = {'marine.json': {"marine": {"fake": True}}}
    monkeypatch.setattr('app.services.weather_service.session.get', make_fake_get(mapping))
    resp = client.get('/weather/marine?q=BayArea')
    assert resp.status_code == 200
    body = resp.json()
    assert body['status'] == 'success'
    assert body['api'] == 'marine'
    assert body['data']['marine']['fake'] is True


def test_marine_by_latlon(monkeypatch):
    disable_cache()
    mapping = {'marine.json': {"marine": {"fake": True}}}
    monkeypatch.setattr('app.services.weather_service.session.get', make_fake_get(mapping))
    resp = client.get('/weather/marine?lat=12.3&lon=45.6')
    assert resp.status_code == 200
    body = resp.json()
    assert body['status'] == 'success'
    assert body['api'] == 'marine'
    assert body['data']['marine']['fake'] is True


def test_search(monkeypatch):
    disable_cache()
    mapping = {'search.json': [{"name": "Delhi"}]}
    monkeypatch.setattr('app.services.weather_service.session.get', make_fake_get(mapping))
    resp = client.get('/weather/search?q=Delhi')
    assert resp.status_code == 200
    body = resp.json()
    assert body['status'] == 'success'
    assert body['api'] == 'search'
    assert isinstance(body['data'], list)
    assert body['data'][0]['name'] == 'Delhi'
