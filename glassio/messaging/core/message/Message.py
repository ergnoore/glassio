from typing import Any
from typing import Mapping


__all__ = [
    "Message",
]


class Message:

    __slots__ = (
        "__headers",
        "__body",
    )

    def __init__(
        self,
        headers: Mapping[str, Any],
        body: bytes
    ) -> None:
        self.__headers = headers
        self.__body = body

    @property
    def headers(self) -> Mapping[str, Any]:
        return self.__headers

    @property
    def body(self) -> bytes:
        return self.__body

    def __repr__(self) -> str:
        return f"Message({self.__headers}, {self.__body})"