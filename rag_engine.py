import os
from groq import Groq
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# ... existing imports ...

class MindGapEngine:
    def __init__(self, api_key, groq_api_key=None):
        self.api_key = api_key
        # Initialize Groq for fast STT
        self.groq_client = Groq(api_key=groq_api_key) if groq_api_key else None
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
        self.llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=self.api_key)
        # ... rest of your init ...

    def transcribe_audio(self, audio_bytes):
        """Converts user voice to text using Whisper via Groq"""
        if not self.groq_client:
            return "Groq API Key missing!"
        
        # Save bytes to a temp file for Whisper
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_bytes)
            
        with open("temp_audio.wav", "rb") as file:
            transcription = self.groq_client.audio.transcriptions.create(
                file=("temp_audio.wav", file.read()),
                model="whisper-large-v3-turbo",
                response_format="text",
            )
        return transcription

    def text_to_speech_logic(self, text):
        """Note: For a hackathon, using a free TTS API or a local gTTS 
        is easiest to deploy on Streamlit Cloud."""
        from gtts import gTTS
        tts = gTTS(text=text, lang='en')
        tts.save("response.mp3")
        return "response.mp3"
