import streamlit as st
from rag_engine import MindGapEngine # Assuming your class name
import os

# 1. Page Configuration
st.set_page_config(page_title="Mind Gap.ai", page_icon="🧠", layout="wide")

# 2. Sidebar for Configuration/API Keys
with st.sidebar:
    st.title("Settings")
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

# 3. Initialize the Backend Engine
@st.cache_resource
def load_engine():
    # This calls your existing rag_engine.py logic
    return MindGapEngine()

engine = load_engine()

# 4. Main UI
st.title("🧠 Mind Gap.ai")
st.markdown("### Close the gap between your notes and your knowledge.")

# File Uploader
uploaded_file = st.file_uploader("Upload your notes (txt or pdf)", type=['txt', 'pdf'])

if uploaded_file:
    # Logic to process the file using your rag_engine
    with st.spinner("Analyzing your notes..."):
        content = uploaded_file.read().decode("utf-8")
        engine.process_document(content)
    st.success("Notes indexed successfully!")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about your notes..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Calling your RAG logic
        response = engine.query(prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
