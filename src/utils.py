import json
import os
import doppler_env
import logging_conf

ENV = {}
DEBUG = False

# put the environment variables in the PATH
for k, v in os.environ.items():
    if k == "DEBUG":
        DEBUG = v == "true"
    ENV[k] = v

logging_conf.set_debug(DEBUG)


def dump_json(data: dict, file: str) -> None:
    with open(file, "w") as f:
        json.dump(data, f, indent=2)


def dump_file(data: str, file: str) -> None:
    with open(file, "w") as f:
        f.write(data)


def read_file(file: str) -> str:
    with open(file, "r") as f:
        return f.read()


if __name__ == "__main__":
    dump_json(ENV, "env.json")
    logging_conf.logger.debug("ENV: %s", ENV)
    print("Done")
