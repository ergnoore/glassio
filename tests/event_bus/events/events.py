from pydantic import BaseModel
from datetime import datetime


__all__ = [
    "BaseEvent",
    "SimpleEvent",
    "EmptyEvent",
    "ImportantEvent",
    "UnserializableEvent",
]


class BaseEvent(BaseModel):
    pass


class EmptyEvent(BaseEvent):
    pass


class SimpleEvent(BaseEvent):
    foo: str
    bar: int


class ImportantEvent(BaseEvent):
    important_field: str


class UnserializableEvent(BaseEvent):
    unserializable_field: datetime = datetime.now()
