import json
import os


MEMORY_DIR = "memory"


def load_memory(filename):

    path = os.path.join(
        MEMORY_DIR,
        filename
    )

    if not os.path.exists(path):

        return {}

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)