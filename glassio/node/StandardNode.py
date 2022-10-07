from glassio.mixins import IStartable


__all__ = [
    "StandardNode",
]


class StandardNode(IStartable):

    __slots__ = ()

    def __init__(self) -> None:
        pass

    async def startup(self) -> None:
        pass

    async def shutdown(self) -> None:
        pass
