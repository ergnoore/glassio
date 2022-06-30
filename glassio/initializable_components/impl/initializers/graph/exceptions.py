from typing import Any
from typing import Optional
from typing import Sequence

from glassio.utils import GlassioException


__all__ = [
    "CycleFoundException",
    "CycleNotFoundException",
]


class CycleFoundException(GlassioException):

    __slots__ = ()

    def __init__(self, cycle: Optional[Sequence[Any]] = None) -> None:
        text = repr(cycle) if cycle is not None else "Unknown cycle."
        super().__init__(text)


class CycleNotFoundException(GlassioException):
    pass
