from .IPlugin import IPlugin


class IPluginFactory:

    __slots__ = ()

    async def __call__(self, *args, **kwargs) -> IPlugin:
        raise NotImplementedError()
