from typing import Optional

import pytest

from glassio.initializable_components import AbstractInitializableComponent
from glassio.initializable_components import InitializableComponentException
from glassio.initializable_components import InitializedState
from glassio.initializable_components import required_state


@pytest.mark.asyncio
async def test_of_required_state_for_async_method():

    class Component(AbstractInitializableComponent):
        def __init__(self) -> None:
            super().__init__()

        @required_state(InitializedState)
        async def method(
            self,
            foo: str,
            bar: Optional[int] = None
        ) -> str:
            return foo + str(bar)

    component = Component()

    with pytest.raises(InitializableComponentException):
        await component.method()


@pytest.mark.asyncio
async def test_of_required_state_for_synchronous_method():

    class Component(AbstractInitializableComponent):
        def __init__(self) -> None:
            super().__init__()

        @required_state(InitializedState)
        def method(
            self,
            foo: str,
            bar: Optional[int] = None
        ) -> str:
            return foo + str(bar)

    component = Component()

    with pytest.raises(InitializableComponentException):
        component.method()
