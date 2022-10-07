from pydantic import BaseModel


__all__ = [
    "RabbitMQConfig",
]


class RabbitMQConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 5672
    login: str = "guest"
    password: str = "guest"
    virtualhost: str = '/'
    ssl: bool = False
    login_method: str = 'PLAIN'
