MindGap AI

## What It Solves

- Students drown in content but miss essentials
- One-size-fits-all education fails everyone
- Nobody knows what they don't know
- Generic resources waste hours of study time

## The Fix

- AI finds your exact knowledge gaps
- Learns your level and adapts automatically
- Reinforces weak spots like a personal tutor
- Zero fluff — only what you need to learn

## Tech Stack

**Frontend**
- React + Vite — Instant loads, fast development
- Tailwind CSS — Clean UI without design headaches

**Backend**
- Flask + SQLite — Lightweight, zero config
- FAISS — Lightning-fast vector search
- Sentence-Transformers — Smart text embeddings
- Groq Llama 3.3 — Fast, intelligent lesson generation

## Project Structure

```
MindGap-AI/
├── backend/
│   ├── app.py          # API routes & request handling
│   ├── rag_engine.py   # FAISS + embeddings + Groq logic
│   └── database.py     # Progress & user data
├── frontend/
│   └── src/
│       ├── App.jsx     # Main app component
│       └── components/ # Reusable UI pieces
```

## Key Features

- **Topic Learning** — Pick a subject, start instantly
- **File Upload** — Drop PDFs, build your knowledge base
- **Progress Dashboard** — See strengths vs. weaknesses
- **Adaptive Lessons** — AI adjusts difficulty in real-time
- **Interactive Quizzes** — Instant feedback on answers
- **Memory Tracking** — System remembers and reinforces weak spots

## Quick Start

**Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
# Add GROQ_API_KEY to .env
python app.py
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
# Open localhost — done!
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/lessons/generate` | POST | Generate lesson for a topic |
| `/api/quiz/generate` | POST | Create quiz questions |
| `/api/quiz/submit` | POST | Submit answers, get feedback |
| `/api/upload` | POST | Upload study materials |
| `/api/progress` | GET | Fetch learning progress |

## Environment Setup

Create `backend/.env`:
```env
GROQ_API_KEY=your_api_key_here
```

