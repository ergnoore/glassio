from ujson import dumps
from ujson import loads

from glassio.messaging import Message

from ..core import IMessagePacker


__all__ = [
    "MessagePackerImpl",
]


class MessagePackerImpl(IMessagePacker):

    """
    Standard message packer.

    Serializes headers as JSON.
    Determining the length of the headers.
    Writes the length of the headers to the first HLB bytes of the result.

    HLB - the number of bytes to store the length of the headers.
    HL - length of headers.

    0               HLB           HLB + HL
    +----------------+----------------+----------------+
    | headers length |     headers    |      body      |
    +----------------+----------------+----------------+

    """

    __slots__ = (
        "__encoding",
        "__headers_length_bytes",
        "__max_headers_length",
    )

    def __init__(self, encoding: str = "utf-8") -> None:
        self.__encoding = encoding
        self.__headers_length_bytes: int = 2  # as a constant
        self.__max_headers_length: int = 256 ** self.__headers_length_bytes - 1

    def pack_message(self, message: Message) -> bytes:
        serialized_headers = dumps(message.headers)
        encoded_headers = serialized_headers.encode(self.__encoding)

        headers_length = len(encoded_headers)

        if headers_length > self.__max_headers_length:
            raise OverflowError("The headers is too long.")

        headers_length_bytes = headers_length.to_bytes(
            self.__headers_length_bytes,
            byteorder="big",
            signed=False
        )
        return headers_length_bytes + encoded_headers + message.body

    def unpack_message(self, packed_message: bytes) -> Message:
        headers_length = int.from_bytes(
            bytes=packed_message[: self.__headers_length_bytes],
            byteorder="big",
            signed=False,
        )
        encoded_headers = packed_message[self.__headers_length_bytes: headers_length + self.__headers_length_bytes]
        serialized_headers = encoded_headers.decode(self.__encoding)

        headers = loads(serialized_headers)
        body = packed_message[headers_length + self.__headers_length_bytes:]

        return Message(
            headers=headers,
            body=body
        )
