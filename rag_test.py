from rag.embedder import create_embedding

from rag.vector_store import (

    add_to_memory,
    total_memories

)

from rag.retriever import search_memory


text1 = "Boss likes Jarvis voice"

text2 = "Boss is studying BS Artificial Intelligence"

text3 = "Boss uses Astra assistant"


add_to_memory(

    create_embedding(text1),

    text1

)

add_to_memory(

    create_embedding(text2),

    text2

)

add_to_memory(

    create_embedding(text3),

    text3

)


print(

    total_memories()

)

print(

    search_memory(

        "What is Boss studying?"

    )

)