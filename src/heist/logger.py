r"""heist Logger
All logger configuration is handled

    >> import logger
    >> _logger = logger.get(__name__)

This establishes a logger in the namespace of the module that writes to the console and a log file.
    Windows:
    ..\heist.log

    Other:
    ../heist.log
"""
import logging
from logging import Formatter, Logger, StreamHandler
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


def setup() -> None:
    """Initialize a logger for the module."""
    _logger: Logger = logging.getLogger()

    if not hasattr(_logger, "setup") or not _logger.setup:
        _logger.propagate = False

        # file logging
        # > format: "2021-03-25 10:28:12,601 msk.<module>: [LEVEL] <message>"
        # > location: "%APPDATA%\mask-tools\logs\msk.log"
        file_handler: TimedRotatingFileHandler = TimedRotatingFileHandler(
            Path(__file__).parents[2].joinpath("heist.log"),
            delay=True,
            when="midnight"
        )

        file_formatter = Formatter(fmt="%(asctime)s %(name)s.%(funcName)s():%(lineno)3s: [%(levelname)s] %(message)s")
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.INFO)

        _logger.addHandler(file_handler)

        # console logging
        console_handler: StreamHandler = StreamHandler()
        console_formatter: Formatter = Formatter(fmt="%(name)s:%(lineno)3s: [%(levelname)s] %(message)s")
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.INFO)

        _logger.addHandler(console_handler)

        _logger.setLevel(logging.INFO)

        _logger.setup = True


def get(namespace: str | None) -> Logger:
    """Gets a namespaced logger.

    Args:
        namespace (str): The namespace of the module, Ex, '__file__'.

    Returns:
        (Logger) The logger in the namespace.
    """
    return logging.getLogger(namespace)
