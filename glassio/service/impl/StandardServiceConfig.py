from typing import Any
from typing import Mapping
from typing import Optional

from pydantic import BaseModel


__all__ = [
    "StandardServiceConfig",
]


class StandardServiceConfig(BaseModel):
    name: str = "glassio-service"
    version: str = "1.0.0"
    settings: Optional[Mapping[str, Any]] = {}
