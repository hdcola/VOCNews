import json
import os
from typing import Dict, Any
import doppler_env
import logging_conf


def init_environment() -> Dict[str, Any]:
    """Initialize environment variables and debug settings.

    Returns:
        Dict[str, Any]: Dictionary containing all environment variables
    """
    env = {}
    debug = False
    for k, v in os.environ.items():
        if k == "DEBUG":
            debug = v.lower() == "true"
        env[k] = v

    logging_conf.set_debug(debug)
    return env


ENV = init_environment()
DEBUG = ENV.get("DEBUG", False)


def dump_json(data: dict, file: str) -> None:
    """Save dictionary data to a JSON file.

    Args:
        data (dict): Data to be saved
        file (str): Target file path

    Raises:
        IOError: If file cannot be written
    """
    try:
        with open(file, "w") as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        logging_conf.logger.error(f"Failed to write JSON file {file}: {e}")
        raise


def load_json(file: str) -> dict:
    """Load data from a JSON file.

    Args:
        file (str): Source file path

    Returns:
        dict: Loaded JSON data

    Raises:
        IOError: If file cannot be read
        json.JSONDecodeError: If file contains invalid JSON
    """
    try:
        with open(file, "r") as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        logging_conf.logger.error(f"Failed to read JSON file {file}: {e}")
        raise


def dump_file(data: str, file: str) -> None:
    """Write string data to a file.

    Args:
        data (str): Data to be written
        file (str): Target file path

    Raises:
        IOError: If file cannot be written
    """
    try:
        with open(file, "w") as f:
            f.write(data)
    except IOError as e:
        logging_conf.logger.error(f"Failed to write file {file}: {e}")
        raise


def read_file(file: str) -> str:
    """Read content from a text file.

    Args:
        file (str): Source file path

    Returns:
        str: File content

    Raises:
        IOError: If file cannot be read
    """
    try:
        with open(file, "r") as f:
            return f.read()
    except IOError as e:
        logging_conf.logger.error(f"Failed to read file {file}: {e}")
        raise


if __name__ == "__main__":
    dump_json(ENV, "env.json")
    logging_conf.logger.debug("ENV: %s", ENV)
    print("Done")
