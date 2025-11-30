import os
import sys
from fastapi.testclient import TestClient

# ---------------------------------------------
# FIX: Ensure project root is added to PYTHONPATH
# ---------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Now Python can find `app.main`
from app.main import app

# Fake DB connection test
def test_db_connection():
    try:
        from app.db import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM dual")  # Oracle heartbeat
        conn.close()
        print("[OK] Database connection successful")
    except Exception as e:
        print("[FAIL] Database connection failed:", e)

client = TestClient(app)

def test_health():
    print("\n[TEST] /health endpoint")
    resp = client.get("/health")
    print("Status:", resp.status_code, "Response:", resp.json())

def test_current_weather_mock():
    print("\n[TEST] /weather/current (mocked)")

    # Fake API response
    class FakeResp:
        def __init__(self):
            self.status_code = 200
            self.url = "https://api.test/current.json?q=Delhi"

        def raise_for_status(self):
            return None

        def json(self):
            return {"current": {"mock": True}}

    # Replace weather API network call
    def fake_get(url, params=None, timeout=None):
        return FakeResp()

    import app.services.weather_service as ws
    ws.session.get = fake_get # type: ignore

    resp = client.get("/weather/current?location=Delhi")
    print("Status:", resp.status_code)
    print("Response:", resp.json())

def test_forecast_mock():
    print("\n[TEST] /weather/forecast (mocked)")

    class FakeResp:
        def __init__(self):
            self.status_code = 200
            self.url = "https://api.test/forecast.json?q=Delhi&days=3"

        def raise_for_status(self):
            return None

        def json(self):
            return {"forecast": {"mock": True}}

    def fake_get(url, params=None, timeout=None):
        return FakeResp()

    import app.services.weather_service as ws
    ws.session.get = fake_get # type: ignore

    resp = client.get("/weather/forecast?q=Delhi&days=3")
    print("Status:", resp.status_code)
    print("Response:", resp.json())

# ---------------------------------------------
# Run all tests without pytest
# ---------------------------------------------
if __name__ == "__main__":
    print("========= Running Full Service Test Suite =========")
    test_db_connection()
    test_health()
    test_current_weather_mock()
    test_forecast_mock()
    print("\n========= Done =========")
