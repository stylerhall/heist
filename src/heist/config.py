import os
from pathlib import Path

import yaml

from heist import logger

_logger = logger.get(__name__)


def _path(loader, node) -> Path | None:
    """Custom constructor for !path tag that resolves a string to a Path-like object.

    Usage in YAML:
        >> path1: !path "../path/to/construct"
        >> path2: !path "c:/path/to/construct"

    Returns:
        (Path | None) The constructed path.
    """
    # Load the sequence into a list
    value = loader.construct_scalar(node)

    if not value:
        return None

    return Path(value).resolve()


def _env_path(loader, node) -> Path | None:
    """Custom constructor for !env_path tag that resolves environment variables to Path-like objects. The first
    item in the index is the environment variable, the rest are path components.

    Usage in YAML:
        >> path1: !env_path ["ENV_VAR", "path", "to", "construct"]

    Returns:
        (Path | None) The constructed path.
    """
    # Load the sequence into a list
    values = loader.construct_sequence(node)

    if not values:
        return None

    # First element is the environment variable
    env_var = values[0]
    # Rest are path components
    path_parts = values[1:]

    base_path: any = os.environ.get(env_var)
    if base_path is None:
        raise ValueError(f"Environment variable '{env_var}' not found")

    full_path = Path(base_path)
    for part in path_parts:
        full_path = full_path / part

    return Path(full_path)


yaml.add_constructor("!path", _path)
yaml.add_constructor("!env_path", _env_path)


def load_settings():
    """Loads the settings from the YAML file."""
    _logger.info("Loading heist settings.")

    with open(Path(__file__).parents[2].joinpath("config", "settings.yaml"), "r") as f:
        return yaml.load(f, Loader=yaml.FullLoader)
