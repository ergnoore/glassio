from typing import Sequence
from typing import Type

from glassio.dispatcher import IFunction
from pydantic import BaseModel

from asterisk_ng.system.chest import Key


__all__ = ["Interface"]


class Interface(BaseModel):
    chest: Sequence[Key] = []
    dispatcher: Sequence[Type[IFunction]] = []

    class Config:
        arbitrary_types_allowed = True
