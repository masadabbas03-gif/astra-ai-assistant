import faiss
import json

from rag.vector_store import (

    index,
    memory_texts

)


def save_index():

    faiss.write_index(

        index,

        "memory/faiss.index"

    )

    with open(

        "memory/vector_memory.json",

        "w",

        encoding="utf-8"

    ) as file:

        json.dump(

            memory_texts,

            file,

            indent=4,

            ensure_ascii=False

        )