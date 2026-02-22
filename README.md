MindGap AI - Adaptive Learning Companion

MindGap AI is a full-stack hackathon project built to identify student knowledge gaps and deliver customized micro-lessons.
Tech Stack
Frontend: React (Vite) + Tailwind CSS
Backend: Flask + SQLite
Vector Search: FAISS
Embeddings: Sentence-Transformers (all-MiniLM-L6-v2)
LLM: Groq API (llama-3.3-70b-versatile)
📂 Project Structure
backend/app.py: Core Flask API.
backend/rag_engine.py: FAISS + SentenceTransformers + Groq.
backend/database.py: SQLite performance monitoring.
frontend/src/App.jsx: Primary interface logic.
frontend/src/components/: Modular UI elements.
💡 Hackathon Demo Tips
Groq Prompting: We leverage llama-3.3-70b-versatile for rapid, high-quality responses.
Micro-learning: The platform assesses user proficiency (beginner/advanced) and tailors lesson depth accordingly.
RAG: Content chunks are indexed locally in FAISS for instant retrieval.
Features
🏠 Home: Start learning by selecting topics.
📁 Notes Upload: Add PDF/Text files to expand your knowledge base.
📊 Dashboard: Monitor progress and identify weak areas.
📖 Micro-lessons: AI-crafted lessons adapted to your skill level.
📝 Quizzes: Engaging MCQs with immediate feedback.
🧠 Memory: Records weak topics to strengthen retention.
Setup Instructions
Backend
Go to the backend folder.
Set up a virtual environment: python -m venv venv.
Activate it: source venv/bin/activate.
Install requirements: pip install -r requirements.txt.
Add your GROQ_API_KEY to a .env file.
Launch the app: python app.py.
Frontend
Go to the frontend folder.
Install packages: npm install.
Start the dev server: npm run dev.
Example Dataset
Demo lecture notes covering "Photosynthesis" or "Quantum Mechanics" (available in data/sample_notes.txt).
