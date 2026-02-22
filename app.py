import streamlit as st
from streamlit_mic_recorder import mic_recorder
from rag_engine import MindGapEngine

# ... existing page config and CSS loading ...

with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    groq_key = st.text_input("Groq API Key (for Voice)", type="password") # Get from console.groq.com

if api_key:
    engine = MindGapEngine(api_key, groq_api_key=groq_key)
    
    # 🎤 VOICE INTERACTION SECTION
    st.write("### 🎙️ Talk to MindGap")
    audio = mic_recorder(
        start_prompt="Click to Speak",
        stop_prompt="Stop & Process",
        key='recorder'
    )

    if audio:
        # 1. Transcribe
        with st.spinner("Listening..."):
            user_text = engine.transcribe_audio(audio['bytes'])
            st.session_state.messages.append({"role": "user", "content": f"🎤 {user_text}"})
        
        # 2. Get AI Response
        with st.spinner("Thinking..."):
            ai_response = engine.query(user_text)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        # 3. Speak Back
        audio_path = engine.text_to_speech_logic(ai_response)
        st.audio(audio_path, format="audio/mp3", autoplay=True)
        st.rerun()

    # ... existing chat display and text input ...
