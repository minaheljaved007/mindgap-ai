import streamlit as st
from streamlit_mic_recorder import mic_recorder
from rag_engine import MindGapEngine

# 1. Advanced Page Setup
st.set_page_config(page_title="MindGap AI", page_icon="🧠", layout="centered")

# 2. Advanced Modern UI (Glassmorphism & Animations)
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #0E1117 0%, #161B22 100%); }
    .stChatFloatingInputContainer { background-color: rgba(255,255,255,0.05) !important; backdrop-filter: blur(10px); }
    .stButton>button {
        border-radius: 20px;
        background: rgba(123, 97, 255, 0.2);
        border: 1px solid #7B61FF;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background: #7B61FF !important;
        box-shadow: 0 0 15px rgba(123, 97, 255, 0.5);
    }
    [data-testid="stChatMessage"] {
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Initialize Engine
if "engine" not in st.session_state:
    if "OPENAI_API_KEY" in st.secrets and "GROQ_API_KEY" in st.secrets:
        st.session_state.engine = MindGapEngine()
    else:
        st.error("Missing API Keys in Streamlit Secrets!")
        st.stop()

engine = st.session_state.engine

# 4. Header Section
st.title("🧠 MindGap AI")
st.caption("Advanced Speech-to-Speech Adaptive Learning")

# 5. Interaction Tabs
tab1, tab2 = st.tabs(["💬 Chat & Voice", "📁 Upload Notes"])

with tab2:
    uploaded_file = st.file_uploader("Upload Notes", type=['txt', 'pdf'])
    if uploaded_file:
        with st.spinner("Analyzing Knowledge Gaps..."):
            content = uploaded_file.read().decode("utf-8")
            engine.process_document(content)
            st.success("Knowledge Base Synced!")

with tab1:
    # Voice Button UI
    col1, col2 = st.columns([1, 4])
    with col1:
        audio = mic_recorder(start_prompt="🎙️", stop_prompt="⏹️", key='mic')
    with col2:
        st.info("Tap the mic to talk to your notes")

    # Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle Audio Input
    if audio:
        user_text = engine.transcribe_audio(audio['bytes'])
        st.session_state.messages.append({"role": "user", "content": user_text})
        
        with st.chat_message("assistant"):
            response = engine.query(user_text)
            st.markdown(response)
            # Inject auto-playing audio
            st.markdown(engine.get_audio_html(response), unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response})

    # Handle Text Input
    if prompt := st.chat_input("Ask anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            response = engine.query(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
