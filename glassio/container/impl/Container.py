from typing import Any
from typing import Generic
from typing import MutableMapping
from typing import Optional
from typing import TypeVar

from ..core import IResolver
from ..core import Key
from ..core import ResolverNotFound
from ..core import UnableToResolveDependency


T = TypeVar('T')


class Container(Generic[T]):

    __slots__ = (
        "__resolvers",
    )

    def __init__(self) -> None:
        self.__resolvers: MutableMapping[Key[T], IResolver[T]] = {}

    def set_resolver(self, key: Key[T], resolver: IResolver[T]) -> None:
        self.__resolvers[key] = resolver

    def resolve(self, key: Key[T], needy: Optional[Any] = None) -> T:

        resolvers = self.__resolvers

        class Proxy:

            def __getattribute__(self, item):
                try:
                    resolver = resolvers[key]
                except KeyError as exc:
                    raise ResolverNotFound(key) from exc

                try:
                    obj = resolver(needy=needy)
                    return getattr(obj, item)
                except Exception as exc:
                    raise UnableToResolveDependency(key) from exc

        return Proxy()

    def delete_resolver(self, key: Key) -> None:
        self.__resolvers.pop(key)