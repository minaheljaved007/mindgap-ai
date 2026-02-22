import streamlit as st
from groq import Groq
from pinecone import Pinecone
import json

class MindGapEngine:

 def __init__(self):

  self.client = Groq(
   api_key=st.secrets["GROQ_API_KEY"]
  )

  self.pc = Pinecone(
   api_key=st.secrets["PINECONE_API_KEY"]
  )

  self.index = self.pc.Index("mindgap")


 def hybrid_search(self,query):

  # keyword filter example
  keyword=query.split()[0]

  result = self.index.query(

   vector=self.embed(query),
   filter={"topic":{"$eq":keyword}},
   top_k=5

  )

  return result
