import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

class MindGapEngine:
    def __init__(self, api_key):
        self.api_key = api_key
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
        self.llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=self.api_key, temperature=0.3)
        self.persist_directory = "./data/chroma_db"
        self.vector_db = None
        
        # Load existing DB if available
        if os.path.exists(self.persist_directory):
            self.vector_db = Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)

    def process_document(self, text_content):
        # Using RecursiveCharacterTextSplitter for better context preservation
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
