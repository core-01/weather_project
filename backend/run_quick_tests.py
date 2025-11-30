from app.main import app
from app.services import weather_service
from app.utils import cache as cache_module
from fastapi.testclient import TestClient

# Disable redis cache for these tests (if configured)
try:
    cache_module._cache._client = None
except Exception:
    pass


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
    """Return a fake_get function that returns different payloads depending on endpoint name."""
    def fake_get(url, params=None, timeout=None):
        # find endpoint name from URL
        if isinstance(url, str):
            end = url.split('/')[-1]
        else:
            end = 'unknown'
        payload = mapping.get(end, {"ok": True})
        return FakeResp(url, payload)
    return fake_get


client = TestClient(app)

mapping = {
    'forecast.json': {"forecast": {"fake": True}},
    'history.json': {"history": {"fake": True}},
    'marine.json': {"marine": {"fake": True}},
    'search.json': [{"name": "Delhi"}],
}

# Monkeypatch the session.get used in weather_service
weather_service.session.get = make_fake_get(mapping)


def run_check(path, expected_api_key=None):
    print(f'CALL {path}')
    resp = client.get(path)
    print(resp.status_code)
    try:
        print(resp.json())
    except Exception as exc:
        print('Failed to read json:', exc)


if __name__ == '__main__':
    print('CALL /health')
    resp = client.get('/health')
    print(resp.status_code)
    print(resp.json())

    run_check('/weather/forecast?q=Delhi&days=3')
    run_check('/weather/history?q=Delhi&dt=2025-11-01')
    run_check('/weather/marine?q=BayArea')
    run_check('/weather/marine?lat=12.3&lon=45.6')
    run_check('/weather/search?q=Delhi')

