__all__ = [
    "IStartable",
]


class IStartable:

    __slots__ = ()

    async def startup(self) -> None:
        raise NotImplementedError()

    async def shutdown(self) -> None:
        raise NotImplementedError()
