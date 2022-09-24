__all__ = [
    "Version",
]


class Version:

    __slots__ = (
        "__major",
        "__minor",
        "__micro",
    )

    def __init__(
        self,
        major: int,
        minor: int = 0,
        micro: int = 0,
    ) -> None:
        self.__major = self.__check_rank(major)
        self.__minor = self.__check_rank(minor)
        self.__micro = self.__check_rank(micro)

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
    def micro(self) -> int:
        return self.__micro

    def __repr__(self) -> str:
        return f"Version({self.__major}.{self.__minor}.{self.__micro})"

    def __str__(self) -> str:
        return f"{self.__major}.{self.__minor}.{self.__micro}"
