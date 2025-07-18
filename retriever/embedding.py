from gemini_api import get_embedding as gemini_embed

def get_embedding(text):
    return gemini_embed(text)