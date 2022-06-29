import pytest

from glassio.initializable_components.impl.initializers.graph.exceptions import CycleNotFoundException
from glassio.initializable_components.impl.initializers.graph.utils import get_cycle


def test_graph_with_cycle() -> None:

    graph = {
        "A": {"B"},
        "B": {"A"}
    }

    print(get_cycle(graph))


def test_graph_with_cycles() -> None:

    graph = {
        "A": {"B"},
        "B": {"C", "F"},
        "F": {"B", "A"},
    }

    get_cycle(graph)


def test_graph_without_cycles() -> None:

    graph = {
        "A": {"B"},
        "B": {"C"},
        "C": {"F", "D", "E"},
    }

    with pytest.raises(CycleNotFoundException):
        get_cycle(graph)
