import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA

class MindGapEngine:
    def __init__(self):
        # We use Streamlit secrets for the API Key
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=self.api_key)
        self.vector_db = None

    def process_document(self, text_content):
        """Processes raw text and adds it to the vector store."""
        # 1. Split text into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.create_documents([text_content])
        
        # 2. Create/Update Vector Store
        self.vector_db = Chroma.from_documents(
            documents=docs, 
            embedding=self.embeddings,
            persist_directory="./data/chroma_db"
        )
        return "Knowledge Base Updated!"

    def query(self, user_question):
        """The RAG Loop: Retrieve relevant chunks and answer."""
        if not self.vector_db:
            return "Please upload some notes first so I have something to think about!"
        
        # 3. Setup Retrieval QA Chain
        retriever = self.vector_db.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever
        )
        
        response = qa_chain.run(user_question)
        return response
