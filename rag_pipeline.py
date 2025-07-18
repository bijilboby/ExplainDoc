from retriever.embedding import get_embedding
from retriever.vector_store import VectorStore
from utils.chunking import chunk_text
from gemini_api import generate_answer

def get_gemini_answer(text, query):
    chunks = chunk_text(text)
    embeddings = [get_embedding(chunk) for chunk in chunks]
    vs = VectorStore()
    vs.add_texts(chunks, embeddings)
    
    query_embedding = get_embedding(query)
    relevant_chunks = vs.query(query_embedding)
    context = "\n".join(relevant_chunks)
    return generate_answer(query, context)
