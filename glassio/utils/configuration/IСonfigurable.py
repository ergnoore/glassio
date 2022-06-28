from typing import Any


class IConfigurable:

    __slots__ = ()

    async def get_config(self) -> Any:
        raise NotImplementedError()

    async def set_config(self, config: Any) -> None:
        raise NotImplementedError()
