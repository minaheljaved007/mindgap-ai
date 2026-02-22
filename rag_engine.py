import os
import streamlit as st
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from groq import Groq
from gtts import gTTS
import base64

class MindGapEngine:
    def __init__(self):
        # Fetching keys from Streamlit Secrets
        self.api_key = st.secrets["OPENAI_API_KEY"]
        self.groq_key = st.secrets.get("GROQ_API_KEY", "")
        
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
        self.llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=self.api_key, temperature=0.3)
        self.vector_db = None

    def process_document(self, text_content):
        # Recursive Chunking for better context preservation
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=150,
            separators=["\n\n", "\n", ".", " "]
        )
        docs = text_splitter.create_documents([text_content])
        
        self.vector_db = Chroma.from_documents(
            documents=docs, 
            embedding=self.embeddings,
            persist_directory="./data/chroma_db"
        )
        return "Knowledge Base Updated!"

    def query(self, user_question):
        if not self.vector_db:
            return "Please upload some notes first!"
        
        retriever = self.vector_db.as_retriever(search_kwargs={"k": 3})
        qa_chain = RetrievalQA.from_chain_type(llm=self.llm, retriever=retriever)
        return qa_chain.run(user_question)

    def transcribe_audio(self, audio_bytes):
        if not self.groq_key: return "Groq API key missing in Secrets."
        client = Groq(api_key=self.groq_key)
        with open("temp.wav", "wb") as f: f.write(audio_bytes)
        with open("temp.wav", "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=("temp.wav", file.read()),
                model="whisper-large-v3-turbo",
                response_format="text",
            )
        return transcription

    def get_audio_html(self, text):
        tts = gTTS(text=text, lang='en')
        tts.save("speech.mp3")
        with open("speech.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            return f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'
