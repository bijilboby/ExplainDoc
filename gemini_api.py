import google.generativeai as genai
import os
import streamlit as st

api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")

def get_embedding(text):
    response = genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="retrieval_query"
    )
    return response["embedding"]

def generate_answer(question, context):
    prompt = f"You are an AI assistant. Use the following context to answer the question.\n\nContext:\n{context}\n\nQuestion: {question}"
    response = model.generate_content(prompt)
    return response.text