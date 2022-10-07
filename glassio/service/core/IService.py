from abc import ABC
from typing import Union
from uuid import UUID

from glassio.dispatcher import IDispatcher
from glassio.event_bus import IEventBus
from glassio.mixins import IStartable
from glassio.utils import Version


__all__ = [
    "IService",
]


class IService(IStartable, ABC):

    __slots__ = ()

    @property
    def name(self) -> str:
        raise NotImplementedError()

    @property
    def instance_id(self) -> Union[UUID, str, int]:
        raise NotImplementedError()

    @property
    def version(self) -> Version:
        raise NotImplementedError()

    @property
    def container(self) -> IEventBus:
        raise NotImplementedError()
