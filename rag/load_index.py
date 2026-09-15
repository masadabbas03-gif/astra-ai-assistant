import os
import json
import faiss


def load_index():
    index_path = "memory/faiss.index"
    memory_path = "memory/vector_memory.json"

    try:
        index = faiss.read_index(index_path)
    except Exception:
        index = faiss.IndexFlatL2(384)

    texts = []
    if os.path.exists(memory_path):
        try:
            with open(memory_path, "r", encoding="utf-8") as file:
                texts = json.load(file)
        except Exception:
            texts = []

    return index, texts