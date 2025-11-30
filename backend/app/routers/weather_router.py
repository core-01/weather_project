from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.services.weather_service import fetch_api_by_name, WeatherAPIError
from app.services.db_service import save_api_response
from app.utils.logger import logger

router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("/current")
def current(location: Optional[str] = Query(None, alias="location")):
    """Convenience endpoint for current weather.

    Example: `/weather/current?location=Delhi`
    """
    if not location:
        raise HTTPException(status_code=400, detail="missing 'location' query parameter")

    try:
        data, meta = fetch_api_by_name("current", location)
        # try to persist but don't fail the API if DB has problems
        try:
            save_api_response(location, "current", data, params={"q": location}, response_time_ms=meta.get("duration_ms"), status_code=meta.get("status_code"), request_url=meta.get("request_url"))
        except Exception as db_exc:
            logger.error("DB save failed for /weather/current: %s", db_exc)

        return {"status": "success", "api": "current", "data": data}
    except WeatherAPIError as e:
        logger.error("WeatherAPIError: %s", e)
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as exc:
        logger.exception("Unexpected error in /weather/current: %s", exc)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/forecast")
def forecast(q: Optional[str] = Query(None), days: int = Query(1, ge=1, le=10)):
    """Convenience endpoint for forecast: `/weather/forecast?q=Delhi&days=3`"""
    if not q:
        raise HTTPException(status_code=400, detail="missing 'q' query parameter")

    try:
        data, meta = fetch_api_by_name("forecast", q, {"days": days})
        try:
            save_api_response(q, "forecast", data, params={"q": q, "days": days}, response_time_ms=meta.get("duration_ms"), status_code=meta.get("status_code"), request_url=meta.get("request_url"))
        except Exception as db_exc:
            logger.error("DB save failed for /weather/forecast: %s", db_exc)

        return {"status": "success", "api": "forecast", "data": data}
    except WeatherAPIError as e:
        logger.error("WeatherAPIError: %s", e)
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as exc:
        logger.exception("Unexpected error in /weather/forecast: %s", exc)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/history")
def history(q: Optional[str] = Query(None), dt: Optional[str] = Query(None)):
    """History endpoint: `/weather/history?q=Delhi&dt=YYYY-MM-DD`"""
    if not q:
        raise HTTPException(status_code=400, detail="missing 'q' query parameter")
    if not dt:
        raise HTTPException(status_code=400, detail="missing 'dt' (date) query parameter")

    # Validate date format YYYY-MM-DD
    from datetime import datetime
    try:
        datetime.strptime(dt, "%Y-%m-%d")
    except Exception:
        raise HTTPException(status_code=400, detail="dt must be in YYYY-MM-DD format")

    try:
        data, meta = fetch_api_by_name("history", q, {"dt": dt})
        try:
            save_api_response(q, "history", data, params={"q": q, "dt": dt}, response_time_ms=meta.get("duration_ms"), status_code=meta.get("status_code"), request_url=meta.get("request_url"))
        except Exception as db_exc:
            logger.error("DB save failed for /weather/history: %s", db_exc)

        return {"status": "success", "api": "history", "data": data}
    except WeatherAPIError as e:
        logger.error("WeatherAPIError: %s", e)
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as exc:
        logger.exception("Unexpected error in /weather/history: %s", exc)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/marine")
def marine(q: Optional[str] = Query(None), lat: Optional[float] = Query(None), lon: Optional[float] = Query(None)):
    """Marine endpoint: `/weather/marine?q=BayArea` or `/weather/marine?lat=12.3&lon=45.6`"""
    if not q and (lat is None or lon is None):
        raise HTTPException(status_code=400, detail="provide 'q' or both 'lat' and 'lon'")

    params = {}
    if q:
        params["q"] = q
    else:
        params["q"] = f"{lat},{lon}"

    try:
        data, meta = fetch_api_by_name("marine", None, params)
        try:
            save_api_response(params.get("q"), "marine", data, params=params, response_time_ms=meta.get("duration_ms"), status_code=meta.get("status_code"), request_url=meta.get("request_url"))
        except Exception as db_exc:
            logger.error("DB save failed for /weather/marine: %s", db_exc)

        return {"status": "success", "api": "marine", "data": data}
    except WeatherAPIError as e:
        logger.error("WeatherAPIError: %s", e)
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as exc:
        logger.exception("Unexpected error in /weather/marine: %s", exc)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/search")
def search(q: Optional[str] = Query(None)):
    """Search/autocomplete endpoint: `/weather/search?q=London`"""
    if not q:
        raise HTTPException(status_code=400, detail="missing 'q' query parameter")

    try:
        data, meta = fetch_api_by_name("search", q)
        try:
            save_api_response(q, "search", data, params={"q": q}, response_time_ms=meta.get("duration_ms"), status_code=meta.get("status_code"), request_url=meta.get("request_url"))
        except Exception as db_exc:
            logger.error("DB save failed for /weather/search: %s", db_exc)

        return {"status": "success", "api": "search", "data": data}
    except WeatherAPIError as e:
        logger.error("WeatherAPIError: %s", e)
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as exc:
        logger.exception("Unexpected error in /weather/search: %s", exc)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/ip")
def ip_lookup(ip: Optional[str] = Query(None)):
    """IP lookup endpoint: `/weather/ip?ip=8.8.8.8` or `/weather/ip?q=8.8.8.8`"""
    if not ip:
        raise HTTPException(status_code=400, detail="missing 'ip' query parameter")
    try:
        data, meta = fetch_api_by_name("ip", ip)
        try:
            save_api_response(ip, "ip", data, params={"q": ip}, response_time_ms=meta.get("duration_ms"), status_code=meta.get("status_code"), request_url=meta.get("request_url"))
        except Exception as db_exc:
            logger.error("DB save failed for /weather/ip: %s", db_exc)

        return {"status": "success", "api": "ip", "data": data}
    except WeatherAPIError as e:
        logger.error("WeatherAPIError: %s", e)
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as exc:
        logger.exception("Unexpected error in /weather/ip: %s", exc)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/timezone")
def timezone(q: Optional[str] = Query(None), lat: Optional[float] = Query(None), lon: Optional[float] = Query(None)):
    """Timezone endpoint: `/weather/timezone?q=New+York` or `/weather/timezone?lat=12.3&lon=45.6`"""
    if not q and (lat is None or lon is None):
        raise HTTPException(status_code=400, detail="provide 'q' or both 'lat' and 'lon'")
    params = {"q": q} if q else {"q": f"{lat},{lon}"}
    try:
        data, meta = fetch_api_by_name("timezone", None, params)
        try:
            save_api_response(params.get("q"), "timezone", data, params=params, response_time_ms=meta.get("duration_ms"), status_code=meta.get("status_code"), request_url=meta.get("request_url"))
        except Exception as db_exc:
            logger.error("DB save failed for /weather/timezone: %s", db_exc)

        return {"status": "success", "api": "timezone", "data": data}
    except WeatherAPIError as e:
        logger.error("WeatherAPIError: %s", e)
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as exc:
        logger.exception("Unexpected error in /weather/timezone: %s", exc)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/astronomy")
def astronomy(q: Optional[str] = Query(None), dt: Optional[str] = Query(None)):
    """Astronomy endpoint: `/weather/astronomy?q=Delhi&dt=2025-11-30`"""
    if not q:
        raise HTTPException(status_code=400, detail="missing 'q' query parameter")
    params = {"q": q}
    if dt:
        params["dt"] = dt
    try:
        data, meta = fetch_api_by_name("astronomy", None, params)
        try:
            save_api_response(q, "astronomy", data, params=params, response_time_ms=meta.get("duration_ms"), status_code=meta.get("status_code"), request_url=meta.get("request_url"))
        except Exception as db_exc:
            logger.error("DB save failed for /weather/astronomy: %s", db_exc)

        return {"status": "success", "api": "astronomy", "data": data}
    except WeatherAPIError as e:
        logger.error("WeatherAPIError: %s", e)
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as exc:
        logger.exception("Unexpected error in /weather/astronomy: %s", exc)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/future")
def future(q: Optional[str] = Query(None), days: Optional[int] = Query(None)):
    """Future endpoint: `/weather/future?q=Delhi&days=7`"""
    if not q:
        raise HTTPException(status_code=400, detail="missing 'q' query parameter")
    params = {}
    if days is not None:
        params["days"] = days
    try:
        data, meta = fetch_api_by_name("future", q, params if params else None)
        try:
            save_api_response(q, "future", data, params=params or None, response_time_ms=meta.get("duration_ms"), status_code=meta.get("status_code"), request_url=meta.get("request_url"))
        except Exception as db_exc:
            logger.error("DB save failed for /weather/future: %s", db_exc)

        return {"status": "success", "api": "future", "data": data}
    except WeatherAPIError as e:
        logger.error("WeatherAPIError: %s", e)
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as exc:
        logger.exception("Unexpected error in /weather/future: %s", exc)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/api/{api_name}")
def generic_api(api_name: str, q: Optional[str] = Query(None), days: Optional[int] = Query(None), dt: Optional[str] = Query(None), ip: Optional[str] = Query(None), lat: Optional[float] = Query(None), lon: Optional[float] = Query(None)):
    """
    Generic endpoint for weather APIs.
    Examples:
      GET /weather/api/current?q=London
      GET /weather/api/forecast?q=Delhi&days=3
    """
    # Build extra params map depending on provided query parameters
    extra = {}
    if days is not None:
        extra["days"] = days
    if dt is not None:
        extra["dt"] = dt
    if ip is not None:
        # some APIs accept IP via 'q'
        extra["q"] = ip
    if lat is not None and lon is not None:
        extra["q"] = f"{lat},{lon}"

    try:
        data, meta = fetch_api_by_name(api_name, q, extra if extra else None)
        # persist (best-effort) — don't let DB errors hide API success
        db_saved = True
        db_error = None
        try:
            save_api_response(q, api_name, data, params=(extra if extra else {"q": q}), response_time_ms=meta.get("duration_ms"), status_code=meta.get("status_code"), request_url=meta.get("request_url"))
        except Exception as db_exc:
            db_saved = False
            db_error = str(db_exc)
            logger.error("DB save failed after successful API call: %s", db_exc)

        resp = {"status": "success", "api": api_name, "data": data}
        if not db_saved:
            resp["db_saved"] = False
            resp["db_error"] = db_error

        return resp
    except WeatherAPIError as e:
        logger.error("WeatherAPIError: %s", e)
        raise HTTPException(status_code=502, detail=str(e))
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException:
        # re-raise HTTPException
        raise
    except Exception as exc:
        logger.exception("Unexpected error in generic_api: %s", exc)
        raise HTTPException(status_code=500, detail="Internal Server Error")
