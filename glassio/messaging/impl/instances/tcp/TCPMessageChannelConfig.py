from pydantic import BaseModel
from pydantic import Field


__all__ = [
    "TCPMessageChannelConfig",
]


class TCPMessageChannelConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = Field(5050, gt=0, lt=65536)
    max_packet_size: int = 1024 * 1024
