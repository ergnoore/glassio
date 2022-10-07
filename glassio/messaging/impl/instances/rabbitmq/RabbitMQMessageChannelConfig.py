from typing import Mapping
from typing import Optional

from pydantic import BaseModel

from .RabbitMQConfig import RabbitMQConfig


__all__ = [
    "RabbitMQMessageChannelConfig",
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


class RabbitMQMessageChannelConfig(BaseModel):
    rabbitmq: RabbitMQConfig = RabbitMQConfig()
    settings_for_publishing: Optional[SettingsForPublishing] = None
    settings_for_consuming: Optional[SettingsForConsuming] = None
