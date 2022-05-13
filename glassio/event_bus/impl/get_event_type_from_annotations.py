from typing import Type
from typing import TypeVar
from typing import Union

from glassio.event_bus.core import IEventHandler


__all__ = [
    "get_event_type_from_annotations",
]


E = TypeVar('E')


def get_event_type_from_annotations(
    handler: Union[IEventHandler[E], Type[IEventHandler[E]]]
) -> E:
    """
    Get event type from IEventHandler annotations.

    :param handler: Handler with event type annotation.
    :raise AttributeError: If handler missing event annotation.
    :type handler: Union[IEventHandler, Type[IEventHandler]
    :return: The type of event for the handler.
    """

    try:
        return handler.__call__.__annotations__["event"]
    except KeyError:
        raise AttributeError("Handler missing event annotation.")
