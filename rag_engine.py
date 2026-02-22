import os
import streamlit as st
from groq import Groq
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from gtts import gTTS
import base64

class MindGapEngine:
    def __init__(self):
        # Automatically pull from Streamlit Secrets
        self.openai_key = st.secrets["OPENAI_API_KEY"]
        self.groq_key = st.secrets["GROQ_API_KEY"]
        
        # Initialize Clients
        self.groq_client = Groq(api_key=self.groq_key)
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.openai_key)
        self.llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=self.openai_key, temperature=0.3)
        
        self.persist_directory = "./data/chroma_db"
        self.vector_db = self._load_db()

    def _load_db(self):
        if os.path.exists(self.persist_directory):
            return Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)
        return None

    def process_document(self, text_content):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        docs = text_splitter.create_documents([text_content])
        self.vector_db = Chroma.from_documents(
            documents=docs, 
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        return "🧠 Knowledge Base Updated!"

    def query(self, user_question):
        if not self.vector_db:
            return "Please upload some notes first!"
        retriever = self.vector_db.as_retriever(search_kwargs={"k": 3})
        qa_chain = RetrievalQA.from_chain_type(llm=self.llm, retriever=retriever)
        return qa_chain.run(user_question)

    def transcribe_audio(self, audio_bytes):
        """Ultra-fast transcription using Groq Whisper"""
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_bytes)
        with open("temp_audio.wav", "rb") as file:
            transcription = self.groq_client.audio.transcriptions.create(
                file=("temp_audio.wav", file.read()),
                model="whisper-large-v3-turbo",
                response_format="text",
            )
        return transcription

    def get_audio_html(self, text):
        """Generates an auto-playing audio component for the UI"""
        tts = gTTS(text=text, lang='en')
        tts.save("response.mp3")
        with open("response.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            return f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'
