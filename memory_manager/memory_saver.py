import json
import os


MEMORY_DIR = "memory"


def save_memory(
    filename,
    data
):

    path = os.path.join(
        MEMORY_DIR,
        filename
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )