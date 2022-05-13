import pytest

from glassio.message_bus import IPayloadPacker
from glassio.message_bus import PayloadPackerImpl


@pytest.fixture()
def packer() -> IPayloadPacker:
    return PayloadPackerImpl()


@pytest.mark.parametrize(
    "message, message_type",
    [
        (b"Message", "message_type"),
        (b"Message", None),
        (b"Message", ""),
        (b"", ""),
        (b"", None),
    ]
)
def test_pack_and_unpack(packer, message, message_type) -> None:
    payload = packer.pack_payload(message, message_type)
    unpacked_message, unpacked_message_type = packer.unpack_payload(payload)

    assert unpacked_message == message
    assert unpacked_message_type == message_type


def test_pack_too_long_message_type(packer) -> None:
    message = b"Message"
    message_type = "_" * (256 * 256)

    with pytest.raises(OverflowError):
        packer.pack_payload(message, message_type)
