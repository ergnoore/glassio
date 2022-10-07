from argparse import ArgumentParser

from glassio.node import StandardNodeFactory
from .launch import run_startable
from asyncio import run

if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument(
        "--config", "-c",
        type=str,
        required=False,
        default="config.yaml",
        help="Path to the configuration file."
    )

    parser.add_argument(
        "--env", "-e",
        type=str,
        required=False,
        default=False,
        help="Load environment variables from the `./.env`."
    )

    parser.add_argument(
        "--env-file", "-E",
        type=str,
        required=False,
        default=".env",
        help="Path to the env file."
    )

    parser.add_argument(
        "--instances", "-i",
        type=int,
        required=False,
        default=1,
        help="Launch [instances] node instances."
    )

    namespace = parser.parse_args()
    node = StandardNodeFactory()()
    run(run_startable(node))

