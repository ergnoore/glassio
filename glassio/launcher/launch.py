from asyncio import Event
from asyncio import get_event_loop
from signal import SIGINT

from glassio.mixins import IStartable

__all__ = [
    "run_startable",
]


async def run_startable(startable: IStartable) -> None:
    event_loop = get_event_loop()
    stop_event = Event()
    event_loop.add_signal_handler(SIGINT, stop_event.set)
    await startable.startup()
    await stop_event.wait()
    await startable.shutdown()
