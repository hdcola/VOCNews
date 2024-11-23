from rich.logging import RichHandler
import logging

# create logger
logger = logging.getLogger("vocnews")
logger.setLevel(logging.INFO)


# create a rich handler
rich_handler = RichHandler()
rich_handler.setLevel(logging.INFO)

# create a logging format
# formatter = logging.Formatter(
#     '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter(
    "%(name)s - %(message)s"
)
rich_handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(rich_handler)


def set_debug(debug: bool) -> None:
    if debug:
        logger.setLevel(logging.DEBUG)
        rich_handler.setLevel(logging.DEBUG)
        print("Debug mode")
    else:
        logger.setLevel(logging.INFO)
        rich_handler.setLevel(logging.INFO)
        print("Info mode")


class PackageFilter(logging.Filter):
    def filter(self, record):
        return record.name.split(".")[0] == "vocnews"


rich_handler.addFilter(PackageFilter())
