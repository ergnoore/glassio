from typing import Optional

import pytest

from glassio.initializable_components import AbstractInitializableComponent
from glassio.initializable_components import CreatedState
from glassio.initializable_components import DeinitializedState
from glassio.initializable_components import DeinitializingState
from glassio.initializable_components import InitializableComponentException
from glassio.initializable_components import InitializedState
from glassio.initializable_components import InitializingState


@pytest.mark.asyncio
async def test_abstract_component_health():
    component = AbstractInitializableComponent()

    await component.initialize()
    await component.deinitialize()


@pytest.mark.asyncio
async def test_created_state():
    component = AbstractInitializableComponent()
    assert type(component.state) == CreatedState


@pytest.mark.asyncio
async def test_of_initialized_state():

    component = AbstractInitializableComponent()

    await component.initialize()
    assert type(component.state) == InitializedState
    await component.deinitialize()


@pytest.mark.asyncio
async def test_of_deinitialized_state():

    component = AbstractInitializableComponent()

    await component.initialize()
    await component.deinitialize()
    assert type(component.state) == DeinitializedState


@pytest.mark.asyncio
async def test_of_initialization():
    was_initialization: bool = False

    class Component(AbstractInitializableComponent):
        def __init__(self) -> None:
            super().__init__()

        async def _initialize(self) -> None:
            nonlocal was_initialization
            was_initialization = True

    component = Component()

    await component.initialize()
    assert was_initialization
    await component.deinitialize()


@pytest.mark.asyncio
async def test_of_deinitialization():
    was_deinitialization: bool = False

    class Component(AbstractInitializableComponent):
        def __init__(self) -> None:
            super().__init__()

        async def _deinitialize(self, exception: Optional[Exception] = None) -> None:
            nonlocal was_deinitialization
            was_deinitialization = True

    component = Component()

    await component.initialize()
    await component.deinitialize()
    assert was_deinitialization


@pytest.mark.asyncio
async def test_of_initializing_state():

    class Component(AbstractInitializableComponent):
        def __init__(self) -> None:
            super().__init__()

        async def _initialize(self) -> None:
            assert type(self.state) == InitializingState

    component = Component()

    await component.initialize()
    await component.deinitialize()


@pytest.mark.asyncio
async def test_of_deinitializing_state():

    class Component(AbstractInitializableComponent):
        def __init__(self) -> None:
            super().__init__()

        async def _deinitialize(self, exception: Optional[Exception] = None) -> None:
            assert type(self.state) == DeinitializingState

    component = Component()

    await component.initialize()
    await component.deinitialize()


@pytest.mark.asyncio
async def test_of_exception_raising():

    class MyException(Exception):
        pass

    component = AbstractInitializableComponent()

    await component.initialize()

    with pytest.raises(MyException):
        await component.deinitialize(exception=MyException())


@pytest.mark.asyncio
async def test_of_double_initialize():

    component = AbstractInitializableComponent()

    await component.initialize()
    with pytest.raises(InitializableComponentException):
        await component.initialize()


@pytest.mark.asyncio
async def test_of_double_deinitialize():

    component = AbstractInitializableComponent()

    await component.initialize()

    await component.deinitialize()
    with pytest.raises(InitializableComponentException):
        await component.deinitialize()


@pytest.mark.asyncio
async def test_of_deinitialize_in_created_state():

    component = AbstractInitializableComponent()

    with pytest.raises(InitializableComponentException):
        await component.deinitialize()


@pytest.mark.asyncio
async def test_of_initialize_in_deinitializing_state():

    class Component(AbstractInitializableComponent):
        def __init__(self) -> None:
            super().__init__()

        async def _initialize(self) -> None:
            await self.deinitialize()

    component = Component()

    with pytest.raises(InitializableComponentException):
        await component.initialize()


@pytest.mark.asyncio
async def test_of_deinitialize_in_initializing_state():

    class Component(AbstractInitializableComponent):
        def __init__(self) -> None:
            super().__init__()

        async def _deinitialize(self, exception: Optional[Exception] = None) -> None:
            await self.initialize()

    component = Component()
    await component.initialize()

    with pytest.raises(InitializableComponentException):
        await component.deinitialize()
