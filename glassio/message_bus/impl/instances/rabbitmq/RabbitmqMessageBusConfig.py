from typing import Mapping
from typing import Optional

from pydantic import BaseModel

from .RabbitmqConfig import RabbitmqConfig


__all__ = [
    "RabbitmqMessageBusConfig",
]


class SettingsForPublishing(BaseModel):
    exchange_name: str
    routing_key: str
    mandatory = False
    immediate = False
    queue_arguments: Mapping[str, str] = {}


class SettingsForConsuming(BaseModel):
    queue_name: str
    consumer_tag: str = ""
    no_local: bool = False
    no_ack: bool = False
    exclusive: bool = False
    no_wait: bool = False
    arguments: Mapping[str, str] = {}


class RabbitmqMessageBusConfig(BaseModel):
    rabbitmq: RabbitmqConfig = RabbitmqConfig()
    settings_for_publishing: Optional[SettingsForPublishing] = None
    settings_for_consuming: Optional[SettingsForConsuming] = None
