from abc import ABC

from glassio.initializable_components import InitializableComponent

from .IMessageChannel import IMessageChannel


__all__ = [
    "InitializableMessageBus",
]


class InitializableMessageBus(IMessageChannel, InitializableComponent, ABC):

    __slots__ = ()
