from typing import Optional
from typing import Type
from typing import TypeVar

from glassio.utils import GlassioException


__all__ = [
    "IState",
    "InitializableComponent",
    "InitializableComponentException",
    "IStateMachine",
    "IStateFactory",
]


class InitializableComponentException(GlassioException):
    pass


class IState:

    __slots__ = ()

    async def initialize(self) -> None:
        """
        Delegate initialization to state.

        :raise InitializableComponentException.
        """
        raise NotImplementedError()

    async def deinitialize(self, exception: Optional[Exception] = None) -> None:
        """
        Delegate deinitialization to state.

        :raise InitializableComponentException.
        """
        raise NotImplementedError()


class InitializableComponent:

    __slots__ = ()

    @property
    def state(self) -> IState:
        """Get current state."""
        raise NotImplementedError()

    async def initialize(self) -> None:
        """
        Initialize the component.

        :raise InitializableComponentException.
        """
        raise NotImplementedError()

    async def deinitialize(self, exception: Optional[Exception] = None) -> None:
        """
        Deinitialize the component.

        When the component is deinitialized,
        the specified exception will be thrown.

        :raise InitializableComponentException.
        """
        raise NotImplementedError()


class IStateMachine:
    """
    Component state machine.

    Stores a state graph and navigates through it.
    """

    __slots__ = ()

    @property
    def state(self) -> IState:
        """Get current state."""
        raise NotImplementedError()

    def next(self) -> IState:
        """
        Move the state machine to the next state.

        :raise StopIteration: If the next state is not defined.
        """
        raise NotImplementedError()


T = TypeVar('T', bound=IState)


class IStateFactory:

    """Creates a state of the given type."""

    __slots__ = ()

    def get_instance(self, state_type: Type[T]) -> T:
        """Instantiate the state."""
        raise NotImplementedError()
