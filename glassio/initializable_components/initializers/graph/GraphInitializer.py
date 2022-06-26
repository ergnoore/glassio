from ...abstract import AbstractInitializableComponent
from ...core import InitializableComponent
from .Graph import Graph


__all__ = [
    "GraphInitializer",
]


class GraphInitializer(AbstractInitializableComponent):

    __slots__ = ()

    def __init__(self, graph: Graph[InitializableComponent]) -> None:
        graph = normalize_graph(graph)
        check_cycle(graph)
        super().__init__()
        self.__graph = graph

    async def _initialize(self) -> None:
        async def initialize_node(node: InitializableComponent) -> None:
            for child_node in graph[node]:
                try:
                    await tasks[child_node]
                except:
                    return

            try:
                await node.initialize()
            except CancelledError:
                pass

        graph = self.__graph
        tasks: Dict[InitializableComponent, Task] = {}
        for node in get_nodes(self.__graph):
            tasks[node] = create_task(initialize_node(node))

        if not tasks:
            return

        done, pending = await wait(tasks.values(), return_when=FIRST_EXCEPTION)
        cancel_tasks(pending)

        try:
            await wait_tasks(iter(done))
        except Exception as e:
            try:
                await wait_tasks(iter(pending))
            finally:
                await self._deinitialize(e)
            raise e

    async def _deinitialize(self, exception: Optional[Exception]) -> None:
        async def deinitialize_node(node: InitializableComponent) -> None:
            for parent_node in reversed_graph[node]:
                try:
                    await tasks[parent_node]
                except:
                    continue

            try:
                await node.deinitialize(exception)
            except CancelledError:
                pass

        reversed_graph = reverse_graph(self.__graph)
        tasks: Dict[InitializableComponent, Task] = {}
        for node in get_nodes(reversed_graph):
            tasks[node] = create_task(deinitialize_node(node))

        if not tasks:
            return

        done, _ = await wait(tasks.values())
        await wait_tasks(iter(done))
