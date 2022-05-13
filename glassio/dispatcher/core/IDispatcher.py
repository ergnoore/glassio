from typing import Any
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Type
from typing import TypeVar

from .functions import IFunction


__all__ = [
    "IDispatcher",
]


F = TypeVar('F', bound=IFunction)


class IDispatcher:

    __slots__ = ()

    def add_function(
        self,
        function_type: Type[F],
        function: F,
        forced: bool = False,
    ) -> None:
        raise NotImplementedError()

    def delete_function(self, function_type: Type[F]) -> None:
        raise NotImplementedError()

    def get_function(self, function_type: Type[F]) -> F:
        raise NotImplementedError()

    async def call_function(
        self,
        function_type: Type[F],
        args: Optional[Sequence[Any]] = None,
        kwargs: Optional[Mapping[str, Any]] = None,
    ) -> Any:
        raise NotImplementedError()
