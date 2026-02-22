import os
import json
import streamlit as st

from groq import Groq
from pinecone import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter


# ==============================
# Helper Functions
# ==============================

PROFILE_PATH = "./data/student_profile.json"


def load_profile():
    os.makedirs("./data", exist_ok=True)

    if not os.path.exists(PROFILE_PATH):
        profile = {
            "name": "Student",
            "weak_topics": [],
            "difficulty": "easy",
            "achievements": [],
            "quiz_scores": []
        }
        save_profile(profile)
        return profile

    with open(PROFILE_PATH, "r") as f:
        return json.load(f)


def save_profile(profile):
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=2)


# ==============================
# Main Engine
# ==============================

class MindGapEngine:

    def __init__(self):

        # ---- GROQ CLIENT ----
        self.client = Groq(
            api_key=st.secrets["GROQ_API_KEY"]
        )

        # ---- PINECONE ----
        self.pc = Pinecone(
            api_key=st.secrets["PINECONE_API_KEY"]
        )

        self.index = self.pc.Index("mindgap")
        self.profile = load_profile()

    # ==============================
    # TEXT CHUNKING (GOOD VERSION)
    # ==============================

    def split_text(self, text):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=900,
            chunk_overlap=150
        )
        docs = splitter.split_text(text)
        return docs

    # ==============================
    # EMBEDDING (1024-D SAFE)
    # ==============================

    def embed(self, text):
        emb = self.client.embeddings.create(
            model="llama-text-embed-v2",  # ✅ MATCHES YOUR 1024 INDEX
            input=text
        )
        return emb.data[0].embedding

    # ==============================
    # DOCUMENT INGESTION
    # ==============================

    def process_document(self, text):
        docs = self.split_text(text)
        vectors = []

        for i, chunk in enumerate(docs):
            vec = self.embed(chunk)

            vectors.append(
                (
                    f"id-{i}",
                    vec,
                    {
                        "text": chunk,
                        "topic": chunk.split(" ")[0].lower()
                    }
                )
            )

        self.index.upsert(vectors)
        return "Knowledge Base Updated"

    # ==============================
    # HYBRID SEARCH (SAFE)
    # ==============================

    def hybrid_search(self, query):
        keyword = query.split(" ")[0].lower()
        embedding = self.embed(query)

        results = self.index.query(
            vector=embedding,
            top_k=6,  # ✅ stronger retrieval
            include_metadata=True,
            filter={
                "topic": {
                    "$eq": keyword
                }
            }
        )

        context_chunks = []

        if "matches" in results:
            for match in results["matches"]:
                if match.get("metadata") and match["metadata"].get("text"):
                    context_chunks.append(match["metadata"]["text"])

        context = "\n\n".join(context_chunks[:5])
        return context

    # ==============================
    # MAIN QA RESPONSE
    # ==============================

    def ask(self, question):
        context = self.hybrid_search(question)
        profile = self.profile

        prompt = f"""
You are MindGap AI, an adaptive learning assistant.

Student Weak Topics:
{profile['weak_topics']}

Difficulty Level:
{profile['difficulty']}

Your job:

1. Identify the learner's knowledge gap
2. Explain clearly in simple terms
3. Provide a short micro-lesson
4. Give one quick practice question

Use ONLY the provided context.
If context is insufficient, say so honestly.

Context:
{context}

Question:
{question}
"""

        completion = self.client.chat.completions.create(
            model="llama3-70b-8192",  # ✅ CORRECT CHAT MODEL
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4
        )

        answer = completion.choices[0].message.content
        return answer

    # ==============================
    # GAP ANALYSIS
    # ==============================

    def gap_analysis(self, student_answer):
        prompt = f"""
Analyse student answer.

Student said:
{student_answer}

Find weak concepts.
Return comma separated weak topics.
"""

        completion = self.client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        weak = completion.choices[0].message.content
        topics = [w.strip() for w in weak.split(",")]

        self.profile["weak_topics"] = list(
            set(self.profile["weak_topics"] + topics)
        )

        save_profile(self.profile)
        return topics

    # ==============================
    # QUIZ GENERATION
    # ==============================

    def generate_quiz(self, topic):
        prompt = f"""
Create 3 short quiz questions.

Difficulty:
{self.profile['difficulty']}

Topic:
{topic}

Return numbered list.
"""

        completion = self.client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return completion.choices[0].message.content

    # ==============================
    # UPDATE SCORE
    # ==============================

    def update_score(self, score):
        self.profile["quiz_scores"].append(score)

        if score > 80:
            self.profile["achievements"].append("⭐ Quick Learner")

        save_profile(self.profile)
