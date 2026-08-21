"""Structured logging configuration for the renderer."""

import logging
import sys

_configured = False


def get_logger(name: str = "renderer") -> logging.Logger:
    """Return a named logger with a consistent formatter.

    Configures the root 'renderer' logger once with a structured
    key=value format suitable for log aggregators.
    """
    global _configured
    logger = logging.getLogger(name)

    if not _configured:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(
            logging.Formatter("%(asctime)s level=%(levelname)s logger=%(name)s %(message)s")
        )
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
        _configured = True

    return logger
