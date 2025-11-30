<!-- .github/copilot-instructions.md - guidance for AI coding agents -->

# Copilot Instructions — weather_project

This file gives concise, actionable guidance for AI coding agents working on this repository.

**Quick Summary**
- **Backend:** FastAPI app under `backend/app` (entry: `backend/app/main.py`).
- **Routers:** `backend/app/routers/*` — routes are thin; business logic lives in `backend/app/services`.
- **Services:** `backend/app/services/*` — network/database access and core logic.
- **DB layer:** `backend/app/db.py` uses `oracledb` and creates a module-level SessionPool if credentials are present. Callers must close connections.

**What to edit & where**
- Add HTTP endpoints in `backend/app/routers/` and call service functions from `backend/app/services/`.
- Serialization / response models live under `backend/app/models/` (Pydantic).
- DB persistence helpers are in `backend/app/services/db_service.py` and use `get_connection()` from `app.db`.

**Key patterns and conventions (do not break)**
- Logging: `app.utils.logger.configure_logging()` is called in `main.py` and the module-level `logger` is used across modules.
- Best-effort DB writes: routers call `save_api_response(...)` but treat DB errors as non-fatal — preserve this behavior unless instructed.
- DB connection lifecycle: `get_connection()` may return a pooled connection or a direct connection; always close/return connections and cursors as current code does.
- External API calls: `app.services.weather_service.call_weather_api()` uses `requests` and raises `WeatherAPIError` on network issues — routers convert these to HTTP 502.
- Allowed API names are defined in `app.services.weather_service.VALID_API_NAMES` — use this set when wiring generic endpoints.

**Environment & runtime**
- Environment variables used (see `backend/app/config.py`):
  - `WEATHER_API_KEY`, `WEATHER_BASE_URL` (defaults to `https://api.weatherapi.com/v1`)
  - Oracle DB: `ORACLE_USER`, `ORACLE_PASSWORD`, `ORACLE_DSN`, optional `ORACLE_POOL_MIN`, `ORACLE_POOL_MAX`, `ORACLE_POOL_INCREMENT`
  - `REQUEST_TIMEOUT` for external requests
- Dev server (from `backend` folder):
```
cd backend
uvicorn app.main:app --reload
```

**Tests**
- A minimal test exists at `backend/tests/test_weather.py` using `fastapi.testclient`.
- To run tests locally (install pytest if missing):
```
cd backend
pip install -r requirements.txt
pip install pytest
python -m pytest tests
```

**Safety & error handling expectations**
- Preserve existing HTTP status mappings: network/API errors -> 502, validation issues -> 400, unexpected exceptions -> 500.
- Do not allow DB errors to mask successful API responses; return API success and include DB failure metadata when relevant.

**Small examples (copyable snippets)**
- Use the service layer for API calls:
```py
from app.services.weather_service import fetch_api_by_name
data = fetch_api_by_name("current", "Delhi")
```
- Save response (best-effort):
```py
try:
    save_api_response("Delhi", "current", data)
except Exception:
    logger.error("DB save failed")
```

**Where to look for more context**
- `backend/app/main.py` — app setup, CORS, router inclusion, health check implementation
- `backend/app/db.py` — pool initialization and `get_connection()` behavior
- `backend/app/services/weather_service.py` — external API integration and allowed endpoints
- `backend/app/services/db_service.py` — example of DB insert and transaction handling
- `backend/app/utils/logger.py` — logging config and `logs/` directory usage

If anything here is unclear or you'd like additional examples (e.g., how to add a new router, or how to mock `oracledb` for tests), tell me which part to expand.
