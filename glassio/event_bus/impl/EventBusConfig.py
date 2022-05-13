from typing import Mapping

from pydantic import BaseModel

from glassio.message_bus import IMessageBus


__all__ = [
    "EventBusConfig",
]


class EventBusConfig(BaseModel):
    number_of_consumers: Mapping[IMessageBus, int] = {}

    class Config:
        arbitrary_types_allowed = True
