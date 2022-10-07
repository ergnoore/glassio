from abc import ABC

from glassio.initializable_components import InitializableComponent

from .IMessageChannel import IMessageChannel


__all__ = [
    "InitializableMessageChannel",
]


class InitializableMessageChannel(IMessageChannel, InitializableComponent, ABC):

    __slots__ = ()
