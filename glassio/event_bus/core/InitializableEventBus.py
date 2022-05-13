from abc import ABC
from typing import TypeVar

from glassio.initializable_components import InitializableComponent

from .IEventBus import IEventBus


__all__ = [
    "InitializableEventBus",
]


E = TypeVar('E')


class InitializableEventBus(IEventBus[E], InitializableComponent, ABC):

    __slots__ = ()
