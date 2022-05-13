from typing import Any

from glassio.utils import GlassioException

from .IEventHandler import IEventHandler


__all__ = [
    "EventBusException",
    "HandlerIsNotAttachedException",
    "EventSerializerException",
    "EventSerializationException",
    "EventDeserializationException",
    "EventDispatchingException",
]


class EventBusException(GlassioException):
    pass


class HandlerIsNotAttachedException(EventBusException):

    def __init__(self, handler: IEventHandler[Any]) -> None:
        super().__init__(
            f"The handler: `{handler}` is not attached."
        )


class EventSerializerException(EventBusException):
    pass


class EventSerializationException(EventSerializerException):
    pass


class EventDeserializationException(EventSerializerException):
    pass


class EventDispatchingException(EventBusException):
    pass
