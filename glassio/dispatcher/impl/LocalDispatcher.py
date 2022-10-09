from inspect import iscoroutinefunction

from typing import MutableMapping
from typing import Type
from typing import TypeVar
from typing import Union

from glassio.logger import ILogger

from ..core import DispatcherException
from ..core import FunctionNotFoundException
from ..core import IDispatcher
from ..core import IFunction


__all__ = [
    "LocalDispatcher"
]


F = TypeVar('F', bound=IFunction)


class LocalDispatcher(IDispatcher):

    __slots__ = (
        "__functions",
        "__function_decorators",
        "__logger",
    )

    def __init__(self, logger: ILogger) -> None:
        self.__functions: MutableMapping[Union[Type[F], str], F] = {}
        self.__logger = logger

    def add_function(
        self,
        alias: Union[Type[F], str],
        function: F,
        public: bool = True
    ) -> None:
        if alias in self.__functions.keys():
            raise DispatcherException(
                "The function has already been added."
            )

        if not isinstance(alias, str):
            if not isinstance(function, alias):
                raise DispatcherException(
                    "The function does not match the specified function_type."
                )

            if not issubclass(alias, IFunction):
                raise DispatcherException(
                    "The specified function_type is not an inheritor of IFunction."
                )

        if not iscoroutinefunction(function.__call__):
            raise DispatcherException(
                "The function must be asynchronous."
            )

        self.__functions[alias] = function

    def delete_function(
        self,
        function_type: Type[F]
    ) -> None:
        try:
            self.__functions.pop(function_type)
        except KeyError:
            raise FunctionNotFoundException(
                f"Unable to delete a non-existent function: `{function_type}`."
            )

    def __get_function(self, function_type: Type[F]) -> F:
        try:
            return self.__functions[function_type]
        except KeyError:
            raise FunctionNotFoundException(
                f"Unable to get a non-existent function: `{function_type}`."
            )

    def get_function(self, function_type: Type[F]) -> F:
        logger = self.__logger
        get_function = self.__get_function

        class FunctionProxy(function_type):

            __slots__ = ()

            async def __call__(self, *args, **kwargs):
                nonlocal function_type, logger, get_function

                function = get_function(function_type)

                try:
                    result = await function(*args, **kwargs)
                except Exception as exc:
                    await logger.debug(
                        f"Call function: `{type(function)}`, args: {args}, kwargs: {kwargs}, "
                        f"exception: `{exc!r}`."
                    )
                    raise exc
                else:
                    await logger.debug(
                        f"Call function: `{type(function)}`, args: {args}, kwargs: {kwargs}, "
                        f"result: `{result!r}`."
                    )
                    return result

        return FunctionProxy()
