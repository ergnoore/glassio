from typing import Any
from typing import Mapping
from typing import Sequence

import pytest
import pytest_asyncio

from glassio.dispatcher import DispatcherException
from glassio.dispatcher import FunctionNotFoundException
from glassio.dispatcher import IFunction
from glassio.dispatcher import IFunctionDecorator


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

        def __call__(self, function: MyFunction) -> IFunction:

            class Wrapper(IFunction):

                async def __call__(self):
                    result = "bar_"
                    result += await function()
                    return result + "_bazz"

            return Wrapper()

    dispatcher.add_function(MyFunction, MyFunctionImpl())
    dispatcher.add_function_decorator(MyFunction, FunctionDecorator())

    result = await dispatcher.call_function(MyFunction)

    assert result == "bar_foo_bazz"


@pytest.mark.asyncio
async def test_deleting_decorator(dispatcher) -> None:

    class FunctionDecorator(IFunctionDecorator[MyFunction]):

        def __call__(self, function: MyFunction) -> IFunction:

            class Wrapper(IFunction):

                async def __call__(self, *args: Sequence[Any], **kwargs: Mapping[str, Any]):
                    raise NotImplementedError()

            return Wrapper()

    dispatcher.add_function(MyFunction, MyFunctionImpl())
    decorator = FunctionDecorator()

    dispatcher.add_function_decorator(MyFunction, decorator)
    dispatcher.delete_function_decorator(MyFunction, decorator)

    result = await dispatcher.call_function(MyFunction)
    assert result == "foo"


@pytest.mark.asyncio
async def test_deleting_nonexistent_decorator(dispatcher) -> None:

    class FunctionDecorator(IFunctionDecorator[MyFunction]):

        def __call__(self, function: MyFunction) -> IFunction:
            raise NotImplementedError()

    with pytest.raises(DispatcherException):
        dispatcher.delete_function_decorator(MyFunction, FunctionDecorator())
