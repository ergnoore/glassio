from typing import Any
from typing import Callable
from typing import Coroutine


__all__ = [
    "IConsumer",
]


IConsumer = Callable[[bytes, str], Coroutine[Any, Any, None]]
