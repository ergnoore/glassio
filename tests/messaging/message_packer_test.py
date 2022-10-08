import pytest

from glassio.messaging import IMessagePacker
from glassio.messaging import Message
from glassio.messaging import MessagePackerImpl


@pytest.fixture()
def packer() -> IMessagePacker:
    return MessagePackerImpl()


@pytest.mark.parametrize(
    "message",
    [
        Message({}, b"message"),
        Message({"foo": "bar", "baz": 123}, b"message"),
        Message({}, b"message" * 1024)
    ]
)
def test_pack_and_unpack(packer, message) -> None:
    packed_message = packer.pack_message(message)
    unpacked_message = packer.unpack_message(packed_message)

    assert unpacked_message.headers == message.headers
    assert unpacked_message.body == message.body


def test_pack_too_long_message_headers(packer) -> None:
    message = Message({"_": "_" * (256 * 256)}, b"message")

    with pytest.raises(OverflowError):
        packer.pack_message(message)
