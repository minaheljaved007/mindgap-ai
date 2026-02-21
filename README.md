MindGap AI – Your Personal Adaptive Learning Buddy
Ever felt like you're drowning in a sea of information but still can't quite grasp the essentials? MindGap AI gets it. That's why we built this application – to help students identify exactly what they don't know and serve up bite-sized, personalized lessons that fill those gaps. Whether you're struggling with photosynthesis or quantum mechanics, this tool adapts to your level and learns alongside you.

The Tech Behind the Magic
We wanted to keep things simple yet powerful for this hackathon build. The frontend comes together with React using Vite for blazing-fast development, styled with Tailwind CSS to look clean without the hassle. On the backend, Flask handles the heavy lifting with a lightweight SQLite database keeping track of your progress.

For the intelligence layer, we leveraged FAISS for lightning-fast vector searches – think of it as giving our app a photographic memory for information retrieval. Sentence-Transformers (specifically the all-MiniLM-L6-v2 model) converts your text into numerical representations that computers can actually work with. And when it comes to generating those personalized lessons? We tapped into Groq's llama-3.3-70b-versatile model for responses that are both quick and remarkably intelligent.

Project Organization
The code lives in a straightforward structure that makes finding your way around easy. The backend/app.py file serves as the heart of our API, handling all the requests coming in from the frontend. Meanwhile, backend/rag_engine.py contains the brains of the operation – that's where FAISS, the embedding model, and Groq integration all work together seamlessly. We tucked the SQLite database logic into backend/database.py to keep performance tracking clean and simple.

On the frontend side, frontend/src/App.jsx contains the main application logic, while the frontend/src/components/ folder holds all the modular UI pieces that make up the interface. This separation makes it easy to tweak one part without breaking another.

Cool Features You'll Actually Want to Use
The home screen welcomes you with a straightforward topic-based learning approach – just pick what you want to learn and get started. If you've got your own study materials, the notes upload feature lets you add PDF or text files to build a knowledge base that feels personal to you. The dashboard gives you a clear view of where you're progressing well and which topics need a little more love.

Here's where things get interesting: the micro-lessons are genuinely adaptive. The AI figures out whether you're a beginner or more advanced, then tailors the depth and complexity of each lesson accordingly. After learning, you can test yourself with interactive quizzes that give instant feedback so you know right away if you've grasped the material. And because we built memory tracking into the system, it remembers which topics give you trouble and reinforces them over time – kind of like having a tutor who actually pays attention.

Getting Everything Running
Setting Up the Backend
First, head into the backend folder and create a virtual environment to keep dependencies organized. Activate it, then install everything listed in the requirements file. You'll need to add your Groq API key to a .env file – this connects your app to the language model that generates those personalized lessons. Once that's done, just run python app.py and your backend should spring to life.

Launching the Frontend
Over in the frontend directory, run npm install to grab all the necessary packages. After that fires up, npm run dev gets your development server running, usually at localhost where you can start playing with the app immediately.
