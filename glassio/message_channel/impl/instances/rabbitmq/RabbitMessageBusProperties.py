from typing import Any
from typing import Mapping
from typing import Optional
from typing import Union


__all__ = [
    "RabbitMessageBusProperties",
    "HEADERS_TYPE",
]


HEADERS_TYPE = Mapping[str, Any]

RabbitMessageBusProperties = Mapping[str, Optional[Union[str, int, HEADERS_TYPE]]]
