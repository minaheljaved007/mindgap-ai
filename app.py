import streamlit as st
import os
import base64
from rag_engine import MindGapEngine
from streamlit_mic_recorder import mic_recorder

# 1. Page Configuration
st.set_page_config(page_title="MindGap AI", page_icon="🧠", layout="wide")

# 2. Advanced Modern UI (CSS)
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0e1117 0%, #161b22 100%); color: white; }
    .stButton>button {
        border-radius: 12px;
        background: rgba(123, 97, 255, 0.2);
        border: 1px solid #7B61FF;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background: #7B61FF !important;
        box-shadow: 0 4px 15px rgba(123, 97, 255, 0.4);
    }
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Initialize Engine using Secrets
@st.cache_resource
def load_engine():
    # Uses st.secrets internally for secure deployment
    return MindGapEngine()

if "OPENAI_API_KEY" in st.secrets:
    engine = load_engine()
else:
    st.error("Please add OPENAI_API_KEY to Streamlit Secrets.")
    st.stop()

# 4. Sidebar Dashboard (Adaptive Logic)
with st.sidebar:
    st.title("📊 Learning Progress")
    if "mastery" not in st.session_state:
        st.session_state.mastery = 0
    st.progress(st.session_state.mastery / 100, text=f"Mastery: {st.session_state.mastery}%")
    st.info("🔥 Streak: 3 Days")
    st.write("---")
    st.write("Settings")
    if st.button("Clear History"):
        st.session_state.messages = []
        st.rerun()

# 5. Main UI Logic
st.title("🧠 MindGap AI")
st.caption("Closing knowledge gaps through adaptive RAG and Voice.")

# Tab Selection for a cleaner UI
tab1, tab2 = st.tabs(["💬 Interactive Learning", "📁 Document Sync"])

with tab2:
    uploaded_file = st.file_uploader("Upload study materials", type=['txt', 'pdf'])
    if uploaded_file:
        with st.spinner("Analyzing gaps..."):
            content = uploaded_file.read().decode("utf-8")
            engine.process_document(content)
            st.success("Notes indexed! You can now start the quiz or chat.")

with tab1:
    # Voice Interaction
    st.write("### 🎙️ Voice Assistant")
    audio = mic_recorder(start_prompt="Speak to AI", stop_prompt="Stop Recording", key='recorder')

    # Chat Interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle Voice Input
    if audio:
        user_text = engine.transcribe_audio(audio['bytes'])
        st.session_state.messages.append({"role": "user", "content": f"🎤 {user_text}"})
        with st.chat_message("user"):
            st.markdown(f"🎤 {user_text}")

        with st.chat_message("assistant"):
            response = engine.query(user_text)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            # Speech-to-Speech: Auto-play the AI response
            audio_html = engine.get_audio_html(response)
            st.markdown(audio_html, unsafe_allow_html=True)

    # Handle Text Input
    if prompt := st.chat_input("Ask a question about your notes..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = engine.query(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
