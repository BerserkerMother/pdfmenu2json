"""
Logging helper module
"""
import logging
import logging.config
import yaml

with open("logger/logging_config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
    logging.captureWarnings(True)


# logging.config.fileConfig(fname="src/logger/logging.conf", disable_existing_loggers=False)


def get_logger(name: str):
    """Logs a message
    Parameters:
        name(str): name of logger
    """
    logger = logging.getLogger(name)
    return logger
