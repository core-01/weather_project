import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field

load_dotenv()

class Settings(BaseSettings):
    ORACLE_USER: str | None = os.getenv("ORACLE_USER")
    ORACLE_PASSWORD: str | None = os.getenv("ORACLE_PASSWORD")
    ORACLE_DSN: str | None = os.getenv("ORACLE_DSN")
    # Connection pool settings (optional). Set in .env as integers.
    ORACLE_POOL_MIN: int | None = int(os.getenv("ORACLE_POOL_MIN", "1"))
    ORACLE_POOL_MAX: int | None = int(os.getenv("ORACLE_POOL_MAX", "4"))
    ORACLE_POOL_INCREMENT: int | None = int(os.getenv("ORACLE_POOL_INCREMENT", "1"))

    WEATHER_API_KEY: str | None = os.getenv("WEATHER_API_KEY")
    WEATHER_BASE_URL: str = os.getenv("WEATHER_BASE_URL", "https://api.weatherapi.com/v1")

    # Tune these if needed
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "10"))

    # Optional Redis cache URL (e.g. redis://localhost:6379/0)
    REDIS_URL: str | None = os.getenv("REDIS_URL")

    # Cache TTL seconds used by optional Redis cache
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "30"))

settings = Settings()
