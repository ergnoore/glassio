from typing import Any
from typing import Callable
from typing import Coroutine
from typing import Optional
from typing import Type

from .core import InitializableComponent
from .core import InitializableComponentException
from .core import IState
from .core import IStateFactory
from .core import IStateMachine

from .states import *


__all__ = [
    "AbstractInitializableComponent",
]


class StandardStateFactory(IStateFactory):

    __slots__ = (
        "__initialize_task",
        "__deinitialize_task",
    )

    def __init__(
        self,
        initialize_task: Callable[[], Coroutine[Any, Any, None]],
        deinitialize_task: Callable[[], Coroutine[Any, Any, None]],
    ) -> None:
        self.__initialize_task = initialize_task
        self.__deinitialize_task = deinitialize_task

    def get_instance(self, state_type: Type[IState]) -> IState:
        if issubclass(state_type, InitializingState):
            return InitializingState(
                self.__initialize_task,
            )
        if issubclass(state_type, DeinitializingState):
            return DeinitializingState(
                self.__deinitialize_task,
            )

        return state_type()


class StandardStateMachine(IStateMachine):

    __slots__ = (
        "__state",
        "__state_factory",
        "__state_graph",
    )

    def __init__(
        self,
        state_factory: IStateFactory,
    ) -> None:
        self.__state_factory = state_factory
        self.__state = self.__state_factory.get_instance(CreatedState)
        self.__state_graph = {
            CreatedState: InitializingState,
            InitializingState: InitializedState,
            InitializedState: DeinitializingState,
            DeinitializingState: DeinitializedState,
            DeinitializedState: InitializingState,
        }

    @property
    def state(self) -> IState:
        return self.__state

    def next(self) -> None:
        try:
            next_state = self.__state_graph[type(self.__state)]
        except KeyError:
            raise StopIteration(
                f"Unknown next state after: {type(self.__state)}."
            )
        self.__state = self.__state_factory.get_instance(next_state)


class AbstractInitializableComponent(InitializableComponent):

    __slots__ = (
        "__state_factory",
        "__state_machine",
        "__name",
    )

    def __init__(self, name: Optional[str] = None) -> None:
        self.__name = name or self.__class__.__name__
        self.__state_factory = StandardStateFactory(
            initialize_task=self._initialize,
            deinitialize_task=self._deinitialize,
        )
        self.__state_machine = StandardStateMachine(
            state_factory=self.__state_factory,
        )

    @property
    def state(self) -> IState:
        return self.__state_machine.state

    async def _initialize(self) -> None:
        """Custom initialization code."""
        pass

    async def initialize(self) -> None:
        while True:
            state = self.__state_machine.state
            await state.initialize()

            try:
                self.__state_machine.next()
            except StopIteration as e:
                raise InitializableComponentException() from e
            new_state = self.__state_machine.state

            if issubclass(type(new_state), InitializedState):
                return

    async def deinitialize(self, exception: Optional[Exception] = None) -> None:
        while True:
            state = self.__state_machine.state
            await state.deinitialize()

            try:
                self.__state_machine.next()
            except StopIteration as e:
                raise InitializableComponentException() from e

            new_state = self.__state_machine.state

            if issubclass(type(new_state), DeinitializedState):
                break

        if exception:
            raise exception

    async def _deinitialize(self, exception: Optional[Exception] = None) -> None:
        """Custom deinitialization code."""
        pass

    def __repr__(self) -> str:
        return self.__name
