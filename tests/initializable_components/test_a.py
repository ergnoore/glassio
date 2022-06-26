from glassio.initializable_components.initializers.graph.Graph import Graph
from glassio.initializable_components.initializers.graph.utils import is_cyclic


def test_cyclick() -> None:

    graph = {
        "A": {"B", "C"},
        "B": {"C", "A"},
        "C": {"D", "E", "F"}
    }

    assert is_cyclic(graph)
