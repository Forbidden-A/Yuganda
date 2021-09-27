import typing
from yuganda.config.models import Config
import yaml
import logging

_LOGGER = logging.getLogger("yuganda.config")


def load_config_file(config_file_path: str) -> typing.Dict:
    """
    Safely loads the given config file with PyYAML.
    Raises an exception if the file isn't found, naturally.
    """
    _LOGGER.debug("Loading raw config file")

    with open(config_file_path) as fp:
        return yaml.safe_load(fp)


def deserialise_raw_config(raw_data: dict) -> Config:
    clean_data = {
        key: value for key, value in raw_data.items() if None not in (key, value)
    }
    return Config.from_dict(clean_data)
