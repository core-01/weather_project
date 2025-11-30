from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.weather_router import router as weather_router
from app.routers import db_router
from app.utils.logger import configure_logging, logger
from app.db import get_pool_info, get_connection

configure_logging()  # ensure logging configured early

app = FastAPI(title="Weather Backend API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(weather_router)
# include db router under /db so /db/test-connection works
app.include_router(db_router.router, prefix="/db")


@app.get("/health")
async def health():
    """Health check with optional DB connectivity and pool information.

    Returns basic application status and, if configured, database pool diagnostics.
    """
    status = {"status": "ok"}

    # include pool info (may indicate pool not initialized)
    try:
        pool_info = get_pool_info()
        status["db_pool"] = pool_info
    except Exception as exc:
        logger.exception("Failed to retrieve pool info: %s", exc)
        status["db_pool_error"] = str(exc)

    # quick DB connectivity check (best-effort)
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM DUAL")
        _ = cur.fetchone()
        cur.close()
        try:
            conn.close()
        except Exception:
            pass
        status["db_connected"] = True
    except Exception as exc:
        logger.exception("DB connectivity check failed in health: %s", exc)
        status["db_connected"] = False
        status["db_error"] = str(exc)

    return status
