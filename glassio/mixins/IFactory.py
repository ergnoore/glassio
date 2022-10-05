from typing import Any
from typing import Generic
from typing import Mapping
from typing import Optional
from typing import TypeVar


__all__ = [
    "IFactory"
]


T = TypeVar('T')


class IFactory(Generic[T]):

    __slots__ = ()

    def __call__(
        self,
        settings: Optional[Mapping[str, Any]] = None,
    ) -> T:
        raise NotImplementedError()
