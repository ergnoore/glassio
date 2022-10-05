from typing import Optional
from typing import Tuple

from ..core import IPayloadPacker


__all__ = [
    "PayloadPackerImpl",
]


class PayloadPackerImpl(IPayloadPacker):

    __slots__ = ()

    __ENCODING = "utf-8"
    __MAX_MESSAGE_TYPE_LENGTH = 256 * 256 - 1
    __HEADERS_LENGTH = 1 + 2

    def pack_payload(self, message: bytes, message_type: Optional[str] = None) -> bytes:
        if message_type is None:
            return b"\x00" + message

        message_type_length = len(message_type)

        if message_type_length > self.__MAX_MESSAGE_TYPE_LENGTH:
            raise OverflowError("The `message_type` is too long.")

        message_type_size = message_type_length.to_bytes(2, byteorder="big", signed=False)
        encoded_message_type = message_type.encode(encoding=self.__ENCODING)
        return b"\x01" + message_type_size + encoded_message_type + message

    def unpack_payload(self, payload: bytes) -> Tuple[bytes, Optional[str]]:

        if not payload[0]:
            return payload[1:], None

        message_type_length = int.from_bytes(
            bytes=payload[1: self.__HEADERS_LENGTH],
            byteorder="big",
            signed=False,
        )

        encoded_message_type = payload[self.__HEADERS_LENGTH: message_type_length + self.__HEADERS_LENGTH]
        message_type = encoded_message_type.decode(encoding=self.__ENCODING)
        return payload[message_type_length + self.__HEADERS_LENGTH:], message_type
