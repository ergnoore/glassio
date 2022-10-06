from typing import Any
from typing import Generic
from typing import Optional
from typing import TypeVar


__all__ = ["IResolver"]


T = TypeVar('T')


class IResolver(Generic[T]):

    __slots__ = ()

    def __call__(self, needy: Optional[Any] = None) -> T:
        raise NotImplementedError()
