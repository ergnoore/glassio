from .StandardNode import StandardNode


__all__ = [
    "StandardNodeFactory",
]


class StandardNodeFactory:

    def __call__(self) -> StandardNode:
        return StandardNode()
