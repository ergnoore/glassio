from argparse import ArgumentParser
from asyncio import get_event_loop
from asyncio import Event
from signal import SIGINT
from glassio.mixins import IStartable


async def run_node(node: IStartable) -> None:
    event_loop = get_event_loop()
    stop_event = Event()
    event_loop.add_signal_handler(SIGINT, stop_event.set)
    await node.startup()
    await stop_event.wait()
    await node.shutdown()


def launch_node() -> None:
    parser = ArgumentParser()
    parser.add_argument("--config-path", type=str, required=False, default="config.yaml")
    parser.add_argument("--load-env", action="store_const", const=True, required=False, default=False)
    parser.add_argument("--group", type=str, required=False, default="plugins")

    namespace = parser.parse_args()
    config_path = Path(namespace.config_path)
    service_initializer_config_path = namespace.service_initializer_config_path
    load_dotenv: bool = namespace.load_dotenv
    group: str = namespace.group

    if load_dotenv:
        dotenv.load_dotenv(dotenv.find_dotenv(usecwd=True))

    run(run_service_async(config_path, service_initializer_config_path, group))
