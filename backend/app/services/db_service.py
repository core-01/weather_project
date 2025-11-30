from typing import Dict, Any, Optional
import json
from app.db import get_connection
from app.utils.logger import logger


def save_api_response(location: Optional[str], api_type: str, payload: Dict[str, Any], params: Optional[Dict[str, Any]] = None, response_time_ms: Optional[int] = None, status_code: Optional[int] = None, request_url: Optional[str] = None) -> None:
    """
    Save the raw JSON payload into weather_api_response table.
    The payload is serialized with `json.dumps` to ensure valid JSON storage.

    New columns `params_json` and `response_time_ms` are populated when provided.
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        json_text = json.dumps(payload)
        params_text = json.dumps(params) if params is not None else None
        try:
            cursor.execute(
                """
                INSERT INTO weather_api_response (location, api_type, json_data, params_json, response_time_ms, status_code, request_url)
                VALUES (:loc, :api, :jsondata, :params, :resp_ms, :status, :url)
                """,
                {
                    "loc": location or "N/A",
                    "api": api_type,
                    "jsondata": json_text,
                    "params": params_text,
                    "resp_ms": response_time_ms,
                    "status": status_code,
                    "url": request_url,
                }
            )
        except Exception as exc:
            # If the extended columns do not exist in the target DB, fallback to older schemas.
            logger.warning("Extended insert failed, attempting fallback insert: %s", exc)
            try:
                cursor.execute(
                    """
                    INSERT INTO weather_api_response (location, api_type, json_data, params_json, response_time_ms)
                    VALUES (:loc, :api, :jsondata, :params, :resp_ms)
                    """,
                    {
                        "loc": location or "N/A",
                        "api": api_type,
                        "jsondata": json_text,
                        "params": params_text,
                        "resp_ms": response_time_ms,
                    }
                )
            except Exception:
                # Last resort: minimal insert
                logger.warning("Fallback insert failed, attempting minimal insert.")
                cursor.execute(
                    """
                    INSERT INTO weather_api_response (location, api_type, json_data)
                    VALUES (:loc, :api, :jsondata)
                    """,
                    {
                        "loc": location or "N/A",
                        "api": api_type,
                        "jsondata": json_text,
                    }
                )
        conn.commit()
    except Exception as exc:
        logger.exception("Failed to save API response: %s", exc)
        raise
    finally:
        if cursor:
            try:
                cursor.close()
            except Exception:
                pass
        if conn:
            try:
                conn.close()
            except Exception:
                pass
