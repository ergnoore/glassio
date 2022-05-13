from abc import ABC

from glassio.initializable_components import InitializableComponent

from .IMessageBus import IMessageBus


__all__ = [
    "InitializableMessageBus",
]


class InitializableMessageBus(IMessageBus, InitializableComponent, ABC):

    __slots__ = ()
