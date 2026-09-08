import numpy as np

from rag.embedder import create_embedding
from rag.vector_store import (

    index,
    memory_texts

)


def search_memory(

    query,

    top_k=3

):

    if index.ntotal == 0:

        return []

    query_embedding = create_embedding(

        query

    )

    query_vector = np.array(

        [query_embedding],

        dtype="float32"

    )

    distances, indices = index.search(

        query_vector,

        top_k

    )

    results = []

    for idx in indices[0]:

        if idx < len(

            memory_texts

        ):

            results.append(

                memory_texts[idx]

            )

    return results