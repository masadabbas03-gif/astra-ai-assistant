import faiss
import numpy as np

from rag.load_index import load_index


memory_texts = []

index = load_index()


def add_to_memory(

    embedding,

    text

):

    vector = np.array(

        [embedding],

        dtype="float32"

    )

    index.add(

        vector

    )

    memory_texts.append(

        text

    )


def total_memories():

    return index.ntotal