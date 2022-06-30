from abc import ABC
from typing import Generic
from typing import TypeVar


__all__ = [
    "IConfigurable",
    "IDynamicConfigurable",
]


T = TypeVar('T')


class IConfigurable(Generic[T], ABC):

    __slots__ = ()

    async def get_configuration(self) -> T:
        raise NotImplementedError()


class IDynamicConfigurable(IConfigurable[T], ABC):

    __slots__ = ()

    async def update_config(self, config: T) -> None:
        raise NotImplementedError()
