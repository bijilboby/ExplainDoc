import streamlit as st
from extractors import pdf_extractor, html_extractor, excel_extractor, ppt_extractor
from retriever.embedding import get_embedding
from retriever.vector_store import VectorStore
from rag_pipeline import get_gemini_answer
import os
import tempfile

st.set_page_config(page_title="ExplainDoc", page_icon= "🤖", layout="wide")

st.markdown(
    """
    <style>
    body {
        background-color: #f4fdf4;
        color: #2e7d32;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .chat-bubble {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 12px 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        max-width: 90%;
        margin-bottom: 6px;
        transition: background-color 0.3s;
    }
    .chat-user {
        align-self: flex-end;
        background-color: #d0f0c0;
        color: #1b5e20;
    }
    .chat-assistant {
        align-self: flex-start;
        background-color: #f1f8e9;
        color: #33691e;
        font-style: normal;
    }
    .chat-bubble:hover {
        background-color: #eefbe8;
    }
    .custom-input {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: #f1f8e9;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    .custom-input input[type="text"] {
        flex: 1;
        border: none;
        background: transparent;
        outline: none;
        font-size: 1rem;
        color: #2e7d32;
    }
    .custom-input button {
        background: #66bb6a;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("📑 Document Info")
st.sidebar.markdown("Upload a document to extract and ask questions about it.")

uploaded_file = st.sidebar.file_uploader("📤 Upload Document", type=["pdf", "html", "xlsx", "pptx"])

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.document_text = ""
    st.session_state.filename = ""

st.title("💬 ExplainDoc")
st.markdown("Interact with your document like you do with ChatGPT.")

# Upload and process document
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(uploaded_file.read())
        file_path = temp.name

    if uploaded_file.name.endswith(".pdf"):
        text = pdf_extractor.extract_text(file_path)
    elif uploaded_file.name.endswith(".html"):
        text = html_extractor.extract_text(file_path)
    elif uploaded_file.name.endswith(".xlsx"):
        text = excel_extractor.extract_text(file_path)
    elif uploaded_file.name.endswith(".pptx"):
        text = ppt_extractor.extract_text(file_path)
    else:
        st.error("Unsupported file type.")
        st.stop()

    st.session_state.document_text = text
    st.session_state.filename = uploaded_file.name

if st.session_state.filename:
    st.sidebar.markdown(f"**File Name:** `{st.session_state.filename}`")
    st.sidebar.markdown(f"**Content Length:** {len(st.session_state.document_text)} characters")
    st.sidebar.markdown(f"**Previous Q&A:** {len(st.session_state.chat_history)} interactions")

# Chat input interface
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### 🗨️ Ask your question below:")

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("", placeholder="Type your message...", label_visibility="collapsed")
    submit = st.form_submit_button("➡️")

if submit and user_input and st.session_state.document_text:
    with st.spinner("💡 Thinking..."):
        answer = get_gemini_answer(st.session_state.document_text, user_input)
    st.session_state.chat_history.append((user_input, answer))

# Display chat history
if st.session_state.chat_history:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for user_msg, bot_msg in st.session_state.chat_history:
        st.markdown(f'<div class="chat-bubble chat-user"><b>You:</b><br>{user_msg}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-bubble chat-assistant"><b>Assistant:</b><br><i>{bot_msg}</i></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)



