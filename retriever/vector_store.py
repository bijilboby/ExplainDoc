import faiss
import numpy as np

class VectorStore:
    def __init__(self):
        self.index = faiss.IndexFlatL2(768)
        self.texts = []

    def add_texts(self, texts, embeddings):
        self.index.add(np.array(embeddings).astype("float32"))
        self.texts.extend(texts)

    def query(self, query_embedding, k=5):
        D, I = self.index.search(np.array([query_embedding]).astype("float32"), k)
        return [self.texts[i] for i in I[0] if i < len(self.texts)]