from typing import Optional


__all__ = [
    "IDeserializationExceptionHandler",
]


class IDeserializationExceptionHandler:

    __slots__ = ()

    async def __call__(
        self,
        message: bytes,
        message_type: Optional[str],
        exception: Exception,
    ) -> None:
        raise NotImplementedError()
