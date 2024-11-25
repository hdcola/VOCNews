"""
RSS Feed Parser Module

This module handles RSS feed parsing and processing, providing command line interface
for fetching and storing RSS feed data.
"""

import argparse
import utils as ut
from logging_conf import logger
from typing import Namespace

log = logger.getChild(__name__)


def setup_parser() -> Namespace:
    """
    Set up and configure command line argument parser.

    Returns:
        Namespace: Parsed command line arguments
    """
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

    try:
        args = parser.parse_args()
        log.debug(f"start feedrss with args: {args}")

        # Update environment variables with parsed arguments
        for key, value in vars(args).items():
            if key != "version":
                ut.ENV[key] = value

        return args
    except Exception as e:
        log.error(f"Failed to parse arguments: {str(e)}")
        raise


def main() -> None:
    """Main execution function to fetch and store RSS feed data."""
    try:
        args = setup_parser()

        import lapresse
        import mdb

        lapresse.fetch_rss()
        mdb.insert_one(lapresse.rss)

    except Exception as e:
        log.error(f"Error in main execution: {str(e)}")
        raise


if __name__ == "__main__":
    main()
