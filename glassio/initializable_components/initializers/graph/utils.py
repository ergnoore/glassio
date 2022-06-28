from typing import TypeVar, Optional, Any, Collection, Sequence, Mapping, List, Set, Dict, AbstractSet
from .Graph import Graph
from collections import defaultdict
from typing import MutableSequence
from typing import MutableMapping


__all__ = [
    ""
]


T = TypeVar('T')


def get_vertexes(graph: Graph[T]) -> AbstractSet[T]:
    vertexes = set(graph.keys())
    vertexes.update(*graph.values())
    return vertexes


def normalize_graph(graph: Graph[T]) -> Graph[T]:
    normalized_graph = defaultdict(set)
    normalized_graph.update(graph)
    return normalized_graph


def reverse_graph(graph: Graph[T]) -> Graph[T]:
    return {vv: k for k, v in graph.items() for vv in v}


def get_cycle(graph: Graph[T]) -> Sequence[T]:

    normalized_graph = normalize_graph(graph)
    used_vertexes = set()
    cycle: MutableSequence[T] = []

    def dfs(vertex: T) -> None:
        if vertex in used_vertexes:
            raise Exception("Cycle found.")

        cycle.append(vertex)
        used_vertexes.add(vertex)

        for child_vertex in normalized_graph[vertex]:
            dfs(child_vertex)

        cycle.pop()

    for root in get_vertexes(graph):
        used_vertexes.clear()
        cycle.clear()

        try:
            dfs(root)
        except Exception:  # Cycle found.
            return cycle

    raise Exception("Cycle not found.")


def topological_sort(graph: Graph[T]) -> Sequence[T]:

    try:
        get_cycle(graph)
    except Exception:
        pass
    else:
        raise Exception("Cycle found.")

    normalized_graph = normalize_graph(graph)
    used_vertexes = set()
    sequence = []

    def sort(vertex: T) -> None:

        used_vertexes.add(vertex)

        for child_vertex in normalized_graph[vertex]:

            if child_vertex not in used_vertexes:
                sort(child_vertex)

        sequence.append(vertex)

    for vertex in get_vertexes(graph):
        if vertex not in used_vertexes:
            sort(vertex)

    return sequence
