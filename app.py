import streamlit as st
import os
from rag_engine import MindGapEngine

# 1. Page Config
st.set_page_config(page_title="MindGap AI", page_icon="🧠", layout="centered")

# Load CSS
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 2. Sidebar Settings
with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    if st.button("Clear Database"):
        if os.path.exists("./data"):
            import shutil
            shutil.rmtree("./data")
            st.rerun()

# 3. App Logic
st.title("🧠 MindGap AI")
st.caption("Closing the gap between what's in your notes and what's in your head.")

if api_key:
    engine = MindGapEngine(api_key)
    
    # File Upload Section
    uploaded_file = st.file_uploader("Drop your notes here (txt/pdf)", type=['txt', 'pdf'])
    if uploaded_file:
        with st.spinner("Analyzing Knowledge Gaps..."):
            content = uploaded_file.read().decode("utf-8")
            msg = engine.process_document(content)
            st.toast(msg)

    # Chat Interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about your weak areas..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = engine.query(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.warning("Please enter your OpenAI API Key in the sidebar to begin.")
