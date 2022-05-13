from typing import Optional

from glassio.logger import ILogger

from ...core import IDeserializationExceptionHandler


__all__ = [
    "StandardDeserializationExceptionHandler",
]


class StandardDeserializationExceptionHandler(IDeserializationExceptionHandler):

    __slots__ = (
        "__logger",
    )

    def __init__(self, logger: ILogger) -> None:
        self.__logger = logger

    async def __call__(
        self,
        message: bytes,
        message_type: Optional[str],
        exception: Exception
    ) -> None:
        await self.__logger.error(
            "DeserializationExceptionHandler: message deserialization error. "
            f"message: `{message}`, "
            f"message_type: `{message_type}`.",
            exception=e
        )
