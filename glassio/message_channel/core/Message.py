from typing import Union


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
        body: Union[str, bytes]
    ) -> None:
        self.__headers = headers
        self.__body = body

    def headers(self) -> Mapping[str, Any]:
        return self.__headers

    def body(self) -> Union[str, bytes]:
        return self.__body
