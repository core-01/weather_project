import json
from typing import Optional
from app.config import settings
from app.utils.logger import logger


class RedisCache:
    def __init__(self):
        self._client = None
        if settings.REDIS_URL:
            try:
                import redis
                self._client = redis.from_url(settings.REDIS_URL)
            except Exception as exc:
                logger.warning("Redis not available: %s", exc)

    def get(self, key: str) -> Optional[dict]:
        if not self._client:
            return None
        try:
            raw = self._client.get(key)
            if not raw:
                return None
            return json.loads(raw)
        except Exception as exc:
            logger.warning("Redis get failed: %s", exc)
            return None

    def set(self, key: str, value: dict, ttl: int = 30) -> None:
        if not self._client:
            return
        try:
            self._client.set(key, json.dumps(value), ex=ttl)
        except Exception as exc:
            logger.warning("Redis set failed: %s", exc)


_cache = RedisCache()


def get_cache():
    return _cache
