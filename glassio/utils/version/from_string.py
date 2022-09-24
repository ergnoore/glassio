from .Version import Version


__all__ = [
    "from_string",
]


def from_string(str_version: str) -> Version:
    ranks = str_version.split('.')
    return Version(*ranks)
