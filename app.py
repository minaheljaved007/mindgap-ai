import streamlit as st
import os
from rag_engine import MindGapEngine
from streamlit_mic_recorder import mic_recorder

# 1. Advanced Page Setup
st.set_page_config(page_title="MindGap AI", page_icon="🧠", layout="wide")

# 2. Modern UI Design (Glassmorphism & Custom Styling)
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
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Initialize Engine
@st.cache_resource
def load_engine():
    return MindGapEngine()

if "OPENAI_API_KEY" in st.secrets:
    engine = load_engine()
else:
    st.error("Missing API Keys! Please add OPENAI_API_KEY to Streamlit Secrets.")
    st.stop()

# 4. Sidebar Adaptive Dashboard
with st.sidebar:
    st.title("📊 My Learning")
    if "mastery" not in st.session_state:
        st.session_state.mastery = 35
    st.progress(st.session_state.mastery / 100, text=f"Concept Mastery: {st.session_state.mastery}%")
    st.info("🔥 Current Streak: 3 Days")
    st.write("---")
    st.write("💡 **Gap Identified:** Focus on 'Neural Network Layers'")

# 5. Main Application Logic
st.title("🧠 MindGap AI")
st.caption("Closing knowledge gaps with Voice and Adaptive AI.")

tab1, tab2 = st.tabs(["💬 Voice & Chat", "📁 Sync Documents"])

with tab2:
    uploaded_file = st.file_uploader("Upload Notes (PDF/TXT)", type=['txt', 'pdf'])
    if uploaded_file:
        with st.spinner("Analyzing Knowledge Gaps..."):
            content = uploaded_file.read().decode("utf-8")
            engine.process_document(content)
            st.success("Brain Synced! Start chatting or speaking.")

with tab1:
    # Voice Interaction Component
    st.write("### 🎙️ Voice Assistant")
    audio = mic_recorder(start_prompt="Click to Speak", stop_prompt="Process Voice", key='recorder')

    # Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle Audio/Voice Input
    if audio:
        user_text = engine.transcribe_audio(audio['bytes'])
        st.session_state.messages.append({"role": "user", "content": f"🎤 {user_text}"})
        
        with st.chat_message("assistant"):
            response = engine.query(user_text)
            st.markdown(response)
            # Inject auto-playing speech
            st.markdown(engine.get_audio_html(response), unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

    # Handle Standard Text Input
    if prompt := st.chat_input("Ask a question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            response = engine.query(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
