from . import config, logger

logger.setup()

settings = config.load_settings()
