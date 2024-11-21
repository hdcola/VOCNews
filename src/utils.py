import json

PATH = {}
DEBUG = False


def dump_json(data: dict, file: str) -> None:
    with open(file, "w") as f:
        json.dump(data, f, indent=2)
