from typing import TypeVar, Optional, Any, Collection, Sequence, Mapping, List, Set, Dict, AbstractSet
from .Graph import Graph


__all__ = [
    ""
]


T = TypeVar('T')


def get_vertexes(graph: Graph[T]) -> AbstractSet[T]:
    vertexes = set(graph.keys())
    vertexes.update(graph.values())
    return vertexes


def is_cyclic(graph: Graph) -> bool:

    used_vertex = set()

    def dfs(vertex: T):  # function for dfs
        if vertex in used_vertex:
            return
        used_vertex.add(vertex)
        try:
            for neighbour in graph[vertex]:
                dfs(neighbour)
        except:
            pass
    first = tuple(graph.keys())[0]
    dfs(first)

    return len(used_vertex) == len(get_vertexes(graph))

# def get_nodes(graph: Graph[T]) -> Collection[T]:
#     nodes: Set[T] = set()
#     for k, v in graph.items():
#         nodes.add(k)
#         for i in v:
#             nodes.add(i)
#     return nodes
#
#
# def copy_graph(graph: Graph[T]) -> MutableGraph[T]:
#     return {k: set(v) for k, v in graph.items()}
#
#
# def copy_graph_without_edges(graph: Graph[T]) -> MutableGraph[T]:
#     return {node: set() for node in get_nodes(graph)}
#
#
# def normalize_graph(graph: Graph[T]) -> MutableGraph[T]:
#     graph_copy = copy_graph_without_edges(graph)
#     for k, v in graph.items():
#         graph_copy[k].update(v)
#     return graph_copy
#
#
# def reverse_graph(graph: Graph[T]) -> MutableGraph[T]:
#     reversed_graph = copy_graph_without_edges(graph)
#     for k, v in graph.items():
#         for i in v:
#             reversed_graph[i].add(k)
#     return reversed_graph
#
#
# def find_cycle(graph: Graph[T]) -> Optional[Sequence[T]]:
#     def helper(node: T) -> Optional[Sequence[T]]:
#         if node in visited:
#             return None
#         if node in current_visited:
#             return path[path.index(node):]
#         current_visited.add(node)
#         path.append(node)
#         try:
#             child_nodes = graph[node]
#         except KeyError:
#             return None
#         else:
#             for child_node in child_nodes:
#                 cycle = helper(child_node)
#                 if cycle:
#                     return cycle
#         finally:
#             visited.add(node)
#             current_visited.remove(node)
#             path.pop()
#
#     visited: Set[T] = set()
#     current_visited: Set[T] = set()
#     path: List[T] = []
#     for node in graph:
#         cycle = helper(node)
#         if cycle:
#             return cycle
#
#
# class CycleGraphException(Exception):
#     def __init__(self, cycle: Sequence, *args: Any) -> None:
#         super().__init__(cycle, *args)
#
#     @property
#     def cycle(self) -> Sequence:
#         return self.args[0]
#
#
# def check_cycle(graph: Graph) -> None:
#     cycle = find_cycle(graph)
#     if cycle:
#         raise CycleGraphException(cycle)
#
#
# def topological_sort(graph: Graph[T]) -> Sequence[T]:
#     def helper(node: T) -> Optional[Sequence[T]]:
#         if node in visited:
#             return None
#         if node in current_visited:
#             return path[path.index(node):]
#         current_visited.add(node)
#         path.append(node)
#         try:
#             parent_nodes = reversed_graph[node]
#         except KeyError:
#             return None
#         else:
#             for parent_node in parent_nodes:
#                 cycle = helper(parent_node)
#                 if cycle:
#                     return cycle
#         finally:
#             visited.add(node)
#             current_visited.remove(node)
#             path.pop()
#             sorted_nodes.append(node)
#
#     reversed_graph = reverse_graph(graph)
#     visited: Set[T] = set()
#     current_visited: Set[T] = set()
#     path: List[T] = []
#     sorted_nodes: List[T] = []
#     for node in reversed_graph:
#         cycle = helper(node)
#         if cycle:
#             raise CycleGraphException(cycle[::-1])
#     return sorted_nodes[::-1]
