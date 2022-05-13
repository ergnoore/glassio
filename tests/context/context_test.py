from typing import MutableMapping

from glassio.context import clear_context
from glassio.context import get_context
from glassio.context import set_context
from glassio.context import update_context


def test_get_context() -> None:
    context = get_context()
    assert issubclass(type(context), MutableMapping)


def test_set_context() -> None:
    context_data = {"foo": "bar"}
    set_context(context_data)
    assert get_context() == context_data


def test_context_id() -> None:
    initial_context = get_context()

    context_data = {"foo": "bar"}
    set_context(context_data)

    clear_context()

    new_data = {"foo": "baz"}
    update_context(new_data)

    final_context = get_context()
    assert id(initial_context) == id(final_context)
    assert final_context == new_data
