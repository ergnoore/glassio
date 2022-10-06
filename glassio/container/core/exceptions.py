from glassio.utils import GlassioException

from .Key import Key


__all__ = [
    "UnableToResolveDependency",
    "ResolverNotFound",
]


class ContainerException(GlassioException):
    pass


class UnableToResolveDependency(ContainerException):

    def __init__(self, key: Key) -> None:
        super().__init__(f"Unable to resolve dependency by: {key}.")


class ResolverNotFound(ContainerException):

    def __init__(self, key: Key) -> None:
        super().__init__(f"Resolver for: {key} not found.")
