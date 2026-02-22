import streamlit as st
from streamlit_mic_recorder import mic_recorder
from rag_engine import MindGapEngine

st.set_page_config(page_title="MindGap AI", page_icon="🧠", layout="wide")

# Advanced UI: CSS for Dark Mode, Animations, and Hover Effects
st.markdown("""
    <style>
    .stApp { background: #0E1117; color: white; }
    .stButton>button {
        border-radius: 12px; border: 1px solid #7B61FF;
        background: rgba(123, 97, 255, 0.1); transition: 0.3s;
    }
    .stButton>button:hover {
        background: #7B61FF; transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(123, 97, 255, 0.4);
    }
    /* Glassmorphism for chat */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px); border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize Engine with Secrets
if "engine" not in st.session_state:
    try:
        st.session_state.engine = MindGapEngine()
    except Exception:
        st.error("Please set OPENAI_API_KEY and GROQ_API_KEY in Streamlit Secrets.")
        st.stop()

# Dashboard & Gap Analysis (Point 3 & 5)
with st.sidebar:
    st.title("📊 Student Profile")
    st.progress(65, text="Mastery Level")
    st.write("🔥 3 Day Streak")
    st.info("Weak Topics: Photosynthesis, Mitosis")

st.title("🧠 MindGap AI")

# Voice Section
st.write("### 🎙️ Voice Learning")
audio_input = mic_recorder(start_prompt="Start Speaking", stop_prompt="Process Voice", key='recorder')

if audio_input:
    user_text = st.session_state.engine.transcribe_audio(audio_input['bytes'])
    st.chat_message("user").write(user_text)
    
    with st.chat_message("assistant"):
        response = st.session_state.engine.query(user_text)
        st.write(response)
        st.markdown(st.session_state.engine.text_to_speech(response), unsafe_allow_html=True)

# Standard File Upload
uploaded_file = st.file_uploader("Upload Notes (Point 4)", type=['pdf', 'txt'])
if uploaded_file:
    content = uploaded_file.read().decode("utf-8")
    st.session_state.engine.process_document(content)
    st.success("Knowledge Base Updated!")
    
