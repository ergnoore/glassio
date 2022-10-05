__all__ = [
    "Version",
]


class Version:

    __slots__ = (
        "__major",
        "__minor",
        "__patch",
    )

    def __init__(
        self,
        major: int,
        minor: int = 0,
        patch: int = 0,
    ) -> None:
        self.__major = self.__check_rank(major)
        self.__minor = self.__check_rank(minor)
        self.__patch = self.__check_rank(patch)

    def __check_rank(self, rank: int) -> int:
        if rank < 0:
            raise ValueError(f"Rank {rank} must be greater of zero.")
        return rank

    @property
    def major(self) -> int:
        return self.__major

    @property
    def minor(self) -> int:
        return self.__minor

    @property
    def patch(self) -> int:
        return self.__patch

    def __repr__(self) -> str:
        return f"Version({self.__major}.{self.__minor}.{self.__patch})"

    def __str__(self) -> str:
        return f"{self.__major}.{self.__minor}.{self.__patch}"
