from typing import Type
from typing import TypeVar
from typing import Union

from .functions import IFunction


__all__ = [
    "IDispatcher",
]


F = TypeVar('F', bound=IFunction)


class IDispatcher:

    __slots__ = ()

    def add_function(
        self,
        alias: Union[Type[F], str],
        function: F,
        public: bool = True
    ) -> None:
        raise NotImplementedError()

    def get_function(
        self,
        alias: Union[Type[F], str]
    ) -> F:
        raise NotImplementedError()

    def delete_function(
        self,
        alias: Union[Type[F], str]
    ) -> None:
        raise NotImplementedError()
