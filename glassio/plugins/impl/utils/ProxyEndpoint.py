from typing import Any
from typing import Callable
from typing import Coroutine

from fastapi import Response


Endpoint = Callable[..., Coroutine[Any, Any, Response]]


__all__ = [
    "ProxyEndpoint",
    "create_proxy_endpoint"
]


class ProxyEndpoint:

    __slots__ = (
        "__endpoint",
        "__is_proxying",
    )

    @property
    def is_proxying(self) -> bool:
        return self.__is_proxying

    def set_proxying(self, is_proxying: bool):
        self.__is_proxying = is_proxying

    def __init__(self, endpoint: Endpoint) -> None:
        self.__is_proxying = False
        self.__endpoint = endpoint

    def set_endpoint(self, endpoint: Endpoint) -> None:
        self.__endpoint = endpoint

    async def endpoint(self, *args, **kwargs) -> Response:
        print("AAAAAAAAAAAAAAAAAAAa")
        if not self.__is_proxying:
            raise NotImplementedError(
                "The endpoint is unavailable due to the plugin being unloaded."
            )
        return await self.__endpoint(*args, **kwargs)


def create_proxy_endpoint(endpoint: Any) -> ProxyEndpoint:
    obj = ProxyEndpoint(endpoint)
    return obj
