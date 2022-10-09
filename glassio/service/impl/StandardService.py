from typing import Union
from uuid import UUID
from uuid import uuid4

from glassio.utils.version import from_string

from .StandardServiceConfig import StandardServiceConfig

from ..core import IService
from ...container import Container
from ...utils import Version


__all__ = [
    "StandardService",
]


class StandardService(IService):

    __slots__ = (
        "__config",
        "__container",
        "__instance_id",
    )

    def __init__(
        self,
        config: StandardServiceConfig,
        container: Container
    ) -> None:
        self.__config = config
        self.__container = container
        self.__instance_id = uuid4()

    @property
    def name(self) -> str:
        return self.__config.name

    @property
    def instance_id(self) -> Union[UUID, str, int]:
        return self.__instance_id

    @property
    def version(self) -> Version:
        return from_string(self.__config.version)

    @property
    def container(self) -> Container:
        return self.__container
