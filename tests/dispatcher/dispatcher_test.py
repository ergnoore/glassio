import pytest

from glassio.dispatcher import DispatcherException
from glassio.dispatcher import FunctionNotFoundException
from glassio.dispatcher import IFunction


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


async def test_call_missing_function(dispatcher) -> None:
    dispatcher.add_function(MyFunction, MyFunctionImpl())
    function = dispatcher.get_function(MyFunction)
    assert await function() == "foo"
