from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--config-path", type=str, required=False, default="config.yaml")
    parser.add_argument("--service-initializer-config-path", required=False, default=None)
    parser.add_argument("--load-dotenv", action="store_const", const=True, required=False, default=False)
    parser.add_argument("--group", type=str, required=False, default="plugins")
    namespace = parser.parse_args()

    config_path = Path(namespace.config_path)
    service_initializer_config_path = namespace.service_initializer_config_path
    load_dotenv: bool = namespace.load_dotenv
    group: str = namespace.group

    if load_dotenv:
        dotenv.load_dotenv(dotenv.find_dotenv(usecwd=True))