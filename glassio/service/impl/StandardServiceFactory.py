from typing import Optional
from typing import Mapping
from typing import Any
from glassio.mixins import IFactory
from ..core import IService
from .StandardServiceConfig import StandardServiceConfig
from .StandardService import StandardService
__all__ = [
    "StandardServiceFactory",
]


class StandardServiceFactory(IFactory[IService]):

    __slots__ = ()

    def __call__(self, settings: Optional[Mapping[str, Any]] = None) -> IService:
        config = StandardServiceConfig(**settings)
        return StandardService(config)
 