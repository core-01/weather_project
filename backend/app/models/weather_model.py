from pydantic import BaseModel
from typing import Any, Dict, Optional

class WeatherResponse(BaseModel):
    location: Optional[Dict[str, Any]] = None
    current: Optional[Dict[str, Any]] = None
    raw: Optional[Dict[str, Any]] = None
