from uuid import UUID
from glassio.utils import Version


__all__ = [
    "IService",
]


class IService:

    __slots__ = ()

    @property
    def uuid(self) -> UUID:
        raise NotImplementedError()

    @property
    def name(self) -> str:
        raise NotImplementedError()

    @property
    def version(self) -> Version:
        raise NotImplementedError()
