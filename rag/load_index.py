import faiss
import json

from rag.vector_store import (

    memory_texts

)


def load_index():

    try:

        index = faiss.read_index(

            "memory/faiss.index"

        )

    except:

        index = faiss.IndexFlatL2(

            384

        )

    try:

        with open(

            "memory/vector_memory.json",

            "r",

            encoding="utf-8"

        ) as file:

            memory_texts.extend(

                json.load(

                    file

                )

            )

    except:

        pass

    return index