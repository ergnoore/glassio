from typing import Any, Mapping, Sequence

import pytest
import pytest_asyncio

from glassio.dispatcher import DispatcherException
from glassio.dispatcher import FunctionNotFoundException
from glassio.dispatcher import IFunction
from glassio.dispatcher import IFunctionDecorator
from glassio.dispatcher.core.decorators import F
from glassio.dispatcher.core.functions import T


class MyFunction(IFunction[str]):
    async def __call__(self) -> str:
        raise NotImplementedError()


class MyFunctionImpl(MyFunction):
    async def __call__(self) -> str:
        return "foo"


def test_add_function(dispatcher) -> None:
    dispatcher.add_function(MyFunction, MyFunctionImpl())


def test_re_adding_function(dispatcher) -> None:
    dispatcher.add_function(MyFunction, MyFunctionImpl())
    with pytest.raises(DispatcherException):
        dispatcher.add_function(MyFunction, MyFunctionImpl())


def test_forced_re_adding_function(dispatcher) -> None:
    dispatcher.add_function(MyFunction, MyFunctionImpl())
    dispatcher.add_function(MyFunction, MyFunctionImpl(), forced=True)


def test_add_not_inherited_function(dispatcher) -> None:
    class Function(IFunction[str]):
        async def __call__(self) -> str:
            raise NotImplementedError()

    class FunctionImpl:
        async def __call__(self) -> str:
            return "foo"

    with pytest.raises(DispatcherException):
        dispatcher.add_function(Function, FunctionImpl())


def test_add_with_not_inherited_function_type(dispatcher) -> None:

    class Function:
        async def __call__(self) -> str:
            raise NotImplementedError()

    class FunctionImpl(Function):
        async def __call__(self) -> str:
            return "foo"

    with pytest.raises(DispatcherException):
        dispatcher.add_function(Function, FunctionImpl())


def test_add_synchronous_function(dispatcher) -> None:
    class SynchronousFunctionImpl(MyFunction):
        def __call__(self) -> str:
            return "foo"

    with pytest.raises(DispatcherException):
        dispatcher.add_function(MyFunction, SynchronousFunctionImpl())


@pytest.mark.asyncio
async def test_get_function(dispatcher) -> None:
    function = MyFunctionImpl()
    dispatcher.add_function(MyFunction, function)
    extracted_function = dispatcher.get_function(MyFunction)
    assert await extracted_function() == "foo"


def test_get_missing_function(dispatcher) -> None:
    dispatcher.get_function(MyFunction)


def test_delete_function(dispatcher) -> None:
    dispatcher.add_function(MyFunction, MyFunctionImpl())
    dispatcher.delete_function(MyFunction)


def test_delete_missing_function(dispatcher) -> None:
    with pytest.raises(FunctionNotFoundException):
        dispatcher.delete_function(MyFunction)


@pytest.mark.asyncio
async def test_call_missing_function(dispatcher) -> None:
    dispatcher.add_function(MyFunction, MyFunctionImpl())
    function = dispatcher.get_function(MyFunction)
    assert await function() == "foo"


@pytest.mark.asyncio
async def test_adding_decorator(dispatcher) -> None:

    class FunctionDecorator(IFunctionDecorator[MyFunction]):

        def __call__(self, function: F) -> IFunction:

            class Wrapper(IFunction):

                async def __call__(self, *args: Sequence[Any], **kwargs: Mapping[str, Any]):
                    result = "bar_"
                    result += await function(*args, **kwargs)
                    return result + "_bazz"

            return Wrapper()

    dispatcher.add_function(MyFunction, MyFunctionImpl())
    dispatcher.add_function_decorator(MyFunction, FunctionDecorator())

    result = await dispatcher.call_function(MyFunction)

    assert result == "bar_foo_bazz"


@pytest.mark.asyncio
async def test_deleting_decorator(dispatcher) -> None:

    class FunctionDecorator(IFunctionDecorator[MyFunction]):

        def __call__(self, function: F) -> IFunction:

            class Wrapper(IFunction):

                async def __call__(self, *args: Sequence[Any], **kwargs: Mapping[str, Any]):
                    result = "bar_"
                    result += await function(*args, **kwargs)
                    return result + "_bazz"

            return Wrapper()

    dispatcher.add_function(MyFunction, MyFunctionImpl())
    decorator = FunctionDecorator()
    dispatcher.add_function_decorator(MyFunction, decorator)

    result = await dispatcher.call_function(MyFunction)
    assert result == "bar_foo_bazz"

    dispatcher.delete_function_decorator(MyFunction, decorator)
    result = await dispatcher.call_function(MyFunction)
    assert result == "foo"
