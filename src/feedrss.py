import argparse
import utils as ut
from logging_conf import logger

log = logger.getChild(__name__)


def setup_parser() -> None:
    parser = argparse.ArgumentParser(description="Feed RSS")
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        help="URL of the RSS feed",
        required=False
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output file",
        required=False
    )
    args = parser.parse_args()
    log.debug(f"start feedrss with args: {args}")

    for k, v in vars(args).items():
        if k != "version":
            ut.ENV[k] = v


if __name__ == "__main__":
    setup_parser()

    import lapresse
    import mdb

    lapresse.fetch_rss()
    mdb.insert_one(lapresse.rss)
