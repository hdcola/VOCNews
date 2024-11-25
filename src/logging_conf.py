"""Logging configuration module for VOCNews.

This module sets up logging with Rich handler and provides utilities to control log levels
and filtering. It configures a logger named 'vocnews' that only shows logs from the vocnews
package namespace.
"""

from rich.logging import RichHandler
import logging

# create logger
logger = logging.getLogger("vocnews")
logger.setLevel(logging.INFO)

# create a rich handler
rich_handler = RichHandler()
rich_handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter("%(name)s - %(message)s")
rich_handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(rich_handler)


def set_debug(debug: bool) -> None:
    """Set the logging level based on debug flag.

    Args:
        debug (bool): If True, sets logging level to DEBUG; if False, sets to INFO.
    """
    level = logging.DEBUG if debug else logging.INFO
    logger.setLevel(level)
    rich_handler.setLevel(level)


class PackageFilter(logging.Filter):
    """Filter that only allows log records from the 'vocnews' package namespace.

    This filter ensures that only log messages from the vocnews package and its
    submodules are processed, filtering out logs from other packages.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter log records based on package name.

        Args:
            record (logging.LogRecord): The log record to be filtered

        Returns:
            bool: True if the record is from the vocnews package, False otherwise
        """
        return record.name.split(".")[0] == "vocnews"


rich_handler.addFilter(PackageFilter())
