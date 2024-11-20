import argparse
import logging
import utils as ut


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
    logging.info(f"start feedrss with args: {args}")

    for k, v in vars(args).items():
        if k == "debug":
            ut.DEBUG = v
        elif k != "version":
            ut.PATH[k] = v


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    setup_parser()
