from typing import Any
import oracledb
from app.config import settings
"""Oracle DB helpers.

This module creates a SessionPool on import (when possible) and exposes
`get_connection()` for callers. Callers must close connections when done.
"""

# module-level pool reference
_pool: oracledb.SessionPool | None = None


def _init_pool() -> None:
    global _pool
    # only initialize pool when credentials present
    if not settings.ORACLE_USER or not settings.ORACLE_PASSWORD or not settings.ORACLE_DSN:
        _pool = None
        return

    try:
        _pool = oracledb.SessionPool(
            user=settings.ORACLE_USER,
            password=settings.ORACLE_PASSWORD,
            dsn=settings.ORACLE_DSN,
            min=settings.ORACLE_POOL_MIN or 1,
            max=settings.ORACLE_POOL_MAX or 4,
            increment=settings.ORACLE_POOL_INCREMENT or 1,
            threaded=True
        )
    except Exception:
        # if pool creation fails, leave pool as None; callers will fall back to connect()
        _pool = None


# initialize pool at import time
_init_pool()


def get_connection() -> Any:
    """
    Return a connection from the session pool if available, otherwise a new direct connection.
    Caller is responsible for closing the connection (if from pool, call `conn.close()` to return it to pool).
    """
    if _pool is not None:
        return _pool.acquire()

    if not settings.ORACLE_USER or not settings.ORACLE_PASSWORD or not settings.ORACLE_DSN:
        raise ValueError("Oracle DB credentials are not configured in environment variables.")

    return oracledb.connect(
        user=settings.ORACLE_USER,
        password=settings.ORACLE_PASSWORD,
        dsn=settings.ORACLE_DSN
    )


def get_pool_info() -> dict:
    """Return basic information about the connection pool for diagnostics.

    Does not expose credentials.
    """
    if _pool is None:
        return {"pool_initialized": False}

    return {
        "pool_initialized": True,
        "min": getattr(_pool, "min", settings.ORACLE_POOL_MIN),
        "max": getattr(_pool, "max", settings.ORACLE_POOL_MAX),
        "increment": getattr(_pool, "increment", settings.ORACLE_POOL_INCREMENT),
    }
