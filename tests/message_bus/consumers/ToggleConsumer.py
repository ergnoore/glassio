from typing import Optional

from .SimpleConsumer import SimpleConsumer


__all__ = [
    "ToggleConsumer"
]


class ToggleConsumer(SimpleConsumer):

    def __init__(self) -> None:
        super().__init__()

    async def __call__(self, message: bytes, message_type: Optional[str]) -> None:
        if self.call_counter % 2 == 0:
            self._call_counter += 1
            raise Exception("Message rejected!")

        await super(ToggleConsumer, self).__call__(
            message=message,
            message_type=message_type,
        )
