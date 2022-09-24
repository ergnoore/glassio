import pytest

from glassio.initializable_components import AbstractInitializableComponent
from glassio.initializable_components.impl.initializers.graph import GraphInitializer
from glassio.initializable_components.impl.initializers.graph.exceptions import CycleNotFoundException
from glassio.initializable_components.impl.initializers.graph.utils import get_cycle
from glassio.initializable_components.impl.initializers.graph.utils import topological_sort


@pytest.mark.asyncio
async def test_initializer() -> None:
    initializer = GraphInitializer(
        {
            AbstractInitializableComponent(): {
                AbstractInitializableComponent("dependency")
            }
        }
    )
    await initializer.initialize()


def test_simple() -> None:
    graph = {
        "A": {"B"},
    }
    assert topological_sort(graph) == ["B", "A"]


def test_graph_with_cycle() -> None:

    graph = {
        "A": {"B"},
        "B": {"A"}
    }

    assert set(get_cycle(graph)) == {'B', 'A'}


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
