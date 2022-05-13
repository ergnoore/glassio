from glassio.utils import GlassioException


__all__ = [
    "DispatcherException",
    "FunctionNotFoundException"
]


class DispatcherException(GlassioException):
    pass


class FunctionNotFoundException(DispatcherException):
    pass
