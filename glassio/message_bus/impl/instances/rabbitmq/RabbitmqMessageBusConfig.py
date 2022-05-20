from typing import Literal
from typing import Mapping
from typing import Optional

from pydantic import BaseModel

from .RabbitmqConfig import RabbitmqConfig


__all__ = [
    "RabbitmqMessageBusConfig",
]


class SettingsForPublishing(BaseModel):
    exchange_name: str
    exchange_type: Literal["fanout", "direct", "topics", "headers"] = "direct"
    exchange_durable: bool = False
    exchange_passive: bool = False
    exchange_auto_delete: bool = False
    exchange_no_wait: bool = False
    exchange_arguments: Mapping[str, str] = {}

    routing_key: str

    queue_name: Optional[str] = None
    queue_durable: bool = True
    queue_exclusive: bool = False
    queue_auto_delete: bool = False
    queue_arguments: Mapping[str, str] = {}


class SettingsForConsuming(BaseModel):
    queue_name: str


class RabbitmqMessageBusConfig(BaseModel):
    rabbitmq: RabbitmqConfig = RabbitmqConfig()
    settings_for_publishing: Optional[SettingsForPublishing] = None
    settings_for_consuming: Optional[SettingsForConsuming] = None
