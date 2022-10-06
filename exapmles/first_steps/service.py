from glassio.service import IService


class MyAwesomeService(IService):

    __slots__ = ()

    async def shutdown(self) -> None:
        pass

    async def startup(self) -> None:
        pass
