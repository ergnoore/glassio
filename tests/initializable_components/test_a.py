from glassio.initializable_components.initializers.graph.Graph import Graph
from glassio.initializable_components.initializers.graph.utils import get_cycle
from glassio.initializable_components.initializers.graph.utils import topological_sort


def test_cyclick() -> None:

    graph = {
        "A": {"B", "C"},
        "B": {"C", "A"},
        "C": {"D", "E", "F"}
    }
    print("CCCCCCC", get_cycle(graph))
    print("CCCCCCCa", topological_sort(graph))
