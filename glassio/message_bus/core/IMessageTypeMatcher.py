from typing import Generic
from typing import Optional
from typing import TypeVar


T = TypeVar('T')


class IMessageTypeMatcher(Generic[T]):

    __slots__ = ()

    def match(self, message_type: Optional[str]) -> T:
        raise NotImplementedError()
