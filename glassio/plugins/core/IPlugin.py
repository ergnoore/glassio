class IPlugin:

    __slots__ = ()

    @property
    def name(self) -> str:
        raise NotImplementedError()

    @property
    def version(self) -> str:
        raise NotImplementedError()

    async def upload(self) -> None:
        raise NotImplementedError()

    async def unload(self) -> None:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"Plugin<{self.name}>"
