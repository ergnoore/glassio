from abc import ABC

from .IConsumptionChannel import IConsumptionChannel
from .IPublicationChannel import IPublicationChannel


__all__ = [
    "IMessageChannel",
]


class IMessageChannel(IConsumptionChannel, IPublicationChannel, ABC):

    __slots__ = ()
