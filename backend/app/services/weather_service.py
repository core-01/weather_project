from typing import Dict, Any, Optional, Tuple
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from app.config import settings
from app.utils.logger import logger
from app.utils.cache import get_cache
import json


class WeatherAPIError(Exception):
    """Raised when weather API call fails."""


VALID_API_NAMES = {
    "current",
    "forecast",
    "future",
    "history",
    "marine",
    "search",
    "ip",
    "timezone",
    "astronomy",
}


def _normalize_endpoint(name: str) -> str:
    # Ensure the endpoint (like "current") becomes "current.json"
    return name if name.endswith(".json") else f"{name}.json"


# Configure a session with a small retry policy to handle transient errors and 429s
session = requests.Session()
retries = Retry(total=2, backoff_factor=0.5, status_forcelist=(429, 500, 502, 503, 504))
adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)
session.mount("http://", adapter)


def call_weather_api(endpoint: str, params: Optional[Dict[str, Any]] = None, timeout: Optional[int] = None) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Generic caller for WeatherAPI endpoints.
    Returns a tuple of (json_result, meta) where meta contains status_code, duration_ms and request_url.
    """
    if not settings.WEATHER_BASE_URL:
        raise ValueError("WEATHER_BASE_URL is not configured")
    if not settings.WEATHER_API_KEY:
        raise ValueError("WEATHER_API_KEY is not configured")

    endpoint = _normalize_endpoint(endpoint)
    url = f"{settings.WEATHER_BASE_URL.rstrip('/')}/{endpoint}"

    params = dict(params or {})
    params["key"] = settings.WEATHER_API_KEY

    to = timeout or settings.REQUEST_TIMEOUT

    # attempt to use Redis cache if available
    cache = get_cache()
    cache_key = None
    try:
        key_parts = {**(params or {})}
        cache_key = f"weather:{endpoint}:{json.dumps(key_parts, sort_keys=True)}"
        cached = cache.get(cache_key)
        if cached:
            logger.info("Cache hit for %s", cache_key)
            return cached.get("data"), cached.get("meta")
    except Exception:
        # ignore cache errors
        cache_key = None

    start = time.time()
    try:
        resp = session.get(url, params=params, timeout=to)
        resp.raise_for_status()
        result = resp.json()
        duration_ms = int((time.time() - start) * 1000)
        meta = {"status_code": resp.status_code, "duration_ms": duration_ms, "request_url": resp.url}
        logger.info("Weather API call %s status=%s duration_ms=%s url=%s", endpoint, resp.status_code, duration_ms, resp.url)

        # set cache if enabled
        try:
            if cache_key:
                cache.set(cache_key, {"data": result, "meta": meta}, ttl=settings.CACHE_TTL)
        except Exception:
            pass

        return result, meta
    except requests.RequestException as exc:
        duration_ms = int((time.time() - start) * 1000)
        logger.error("Weather API request failed: %s (duration_ms=%s)", exc, duration_ms)
        raise WeatherAPIError(str(exc)) from exc


def fetch_api_by_name(api_name: str, q: Optional[str] = None, extra: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    if api_name not in VALID_API_NAMES:
        raise ValueError(f"Invalid api_name: {api_name}")

    params: Dict[str, Any] = {}
    if q:
        params["q"] = q
    if extra:
        params.update(extra)

    return call_weather_api(api_name, params)
