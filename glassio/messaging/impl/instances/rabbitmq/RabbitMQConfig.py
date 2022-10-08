from pydantic import BaseModel
from pydantic import Field


__all__ = [
    "RabbitMQConfig",
]


class RabbitMQConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = Field(5672, gt=0, lt=65536)
    login: str = "guest"
    password: str = "guest"
    virtualhost: str = '/'
    ssl: bool = False
    login_method: str = 'PLAIN'
