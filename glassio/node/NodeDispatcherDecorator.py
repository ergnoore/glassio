from typing import Union, Type

from glassio.dispatcher import IDispatcher
from glassio.dispatcher import IFunction
from glassio.dispatcher import FunctionNotFoundException


__all__ = [
    "NodeDispatcherDecorator",
]


class NodeDispatcherDecorator(IDispatcher):

    __slots__ = (
        "__dispatcher",
    )

    def __init__(self, dispatcher: IDispatcher) -> None:
        self.__dispatcher = dispatcher

    def add_function(self, alias: Union[Type[IFunction], str], function: IFunction, public: bool = True) -> None:
        self.__dispatcher.add_function(alias, function)

    def get_function(self, alias: Union[Type[IFunction], str]) -> IFunction:
        try:
            function = self.__dispatcher.get_function(alias)
        except FunctionNotFoundException:
            pass

    def delete_function(self, alias: Union[Type[IFunction], str]) -> None:
        self.__dispatcher.delete_function(alias)
