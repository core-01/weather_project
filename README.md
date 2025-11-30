
![CI](https://github.com/core-01/weather_project/actions/workflows/ci.yml/badge.svg)

# weather_project

FastAPI backend + React frontend scaffold for a Weather proxy service. The backend proxies Weather API endpoints, persists raw responses into a database, and exposes a small set of convenience routes for the frontend.

Quick start:

1. Configure environment variables in `backend/.env` (`WEATHER_API_KEY`, `WEATHER_BASE_URL`, DB credentials, optional `REDIS_URL`).
2. Run the backend:

```powershell
cd backend
uvicorn app.main:app --reload
```

Run tests:

```powershell
cd backend
python -m pytest tests
```


