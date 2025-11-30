from fastapi import APIRouter, HTTPException
from app.db import get_connection
from app.utils.logger import logger

router = APIRouter()


@router.get("/test-connection")
async def test_db():
    """Return a simple DB connectivity check result."""
    conn = None
    try:
        conn = get_connection()
        # simple quick check
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM DUAL")
        _ = cur.fetchone()
        cur.close()
        return {"ok": True}
    except Exception as exc:
        logger.exception("DB connectivity check failed: %s", exc)
        raise HTTPException(status_code=500, detail="Database connectivity error")
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass
