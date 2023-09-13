import sys
import logging
from colorama import Fore


def get_logger(level):
    """Logger ..."""
    logLevel = level

    log_format = logging.Formatter(
        f'[{Fore.YELLOW}Flask Seo{Fore.RESET} - %(levelname)s] [%(asctime)s] - %(message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(logLevel)

    # writing to stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logLevel)
    handler.setFormatter(log_format)
    logger.addHandler(handler)
    return logger
