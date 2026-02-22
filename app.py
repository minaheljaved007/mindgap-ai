import streamlit as st
import os
from rag_engine import MindGapEngine

from streamlit_mic_recorder import mic_recorder

from gtts import gTTS

from PyPDF2 import PdfReader
from PIL import Image
import pytesseract


# ---------------------------
# PAGE CONFIG
# ---------------------------

st.set_page_config(

 page_title="MindGap AI",

 layout="wide",

 initial_sidebar_state="expanded"

)


# ---------------------------
# MODERN CSS UI
# ---------------------------

st.markdown("""

<style>

.stApp{

background:

linear-gradient(

135deg,

#020617,

#0f172a,

#020617);

color:white;

}


/* cards */

.block-container{

background:rgba(255,255,255,0.04);

padding:2rem;

border-radius:20px;

backdrop-filter:blur(20px);

}


/* buttons */

button{

background:

linear-gradient(

45deg,

#7c3aed,

#06b6d4

);

border-radius:12px;

border:none;

transition:0.3s;

}

button:hover{

transform:scale(1.05);

box-shadow:0px 0px 20px cyan;

}


/* input */

textarea,input{

background:#020617 !important;

color:white !important;

border-radius:10px;

}


</style>

""",

unsafe_allow_html=True

)


# ---------------------------
# ENGINE LOAD
# ---------------------------

@st.cache_resource

def load_engine():

 return MindGapEngine()


engine = load_engine()


# ---------------------------
# SIDEBAR DASHBOARD
# ---------------------------

st.sidebar.title("🎓 MindGap Dashboard")


profile = engine.profile


st.sidebar.metric(

"Difficulty",

profile["difficulty"]

)

st.sidebar.write("Weak Topics:")

st.sidebar.write(profile["weak_topics"])


st.sidebar.write("Achievements")

for a in profile["achievements"]:

 st.sidebar.success(a)


# ---------------------------
# TITLE
# ---------------------------

st.title("🚀 MindGap AI Adaptive Tutor")


# ---------------------------
# MULTI MODAL UPLOAD
# ---------------------------

st.subheader("📂 Upload Study Material")


file = st.file_uploader(

"Upload PDF / Image / Notes",

type=["pdf","png","jpg","jpeg","txt"]

)


def extract_text(file):

 if file.type=="application/pdf":

  pdf=PdfReader(file)

  text=""

  for p in pdf.pages:

   text+=p.extract_text()

  return text


 elif "image" in file.type:

  image=Image.open(file)

  text=pytesseract.image_to_string(image)

  return text


 else:

  return file.read().decode("utf-8")



if file:

 text=extract_text(file)

 with st.spinner("Processing Knowledge Base..."):

  result=engine.process_document(text)

 st.success(result)



# ---------------------------
# CHAT SECTION
# ---------------------------

st.subheader("💬 Ask MindGap Tutor")


question = st.text_area(

"Ask your Question"

)


col1,col2,col3=st.columns(3)


# ---------------------------
# ASK BUTTON
# ---------------------------

with col1:

 if st.button("🧠 Ask Tutor"):

  with st.spinner("Thinking..."):

   answer=engine.ask(question)

   st.success(answer)


   # voice reply

   tts=gTTS(answer)

   tts.save("reply.mp3")

   st.audio("reply.mp3")



# ---------------------------
# GAP ANALYSIS
# ---------------------------

with col2:

 if st.button("🔎 Gap Analysis"):

  topics=engine.gap_analysis(question)

  st.warning("Weak Topics Added:")

  st.write(topics)



# ---------------------------
# QUIZ GENERATION
# ---------------------------

with col3:

 if st.button("📝 Generate Quiz"):

  quiz=engine.generate_quiz(question)

  st.info(quiz)



# ---------------------------
# VOICE INPUT
# ---------------------------

st.subheader("🎤 Voice Tutor")


audio = mic_recorder(

start_prompt="Start",

stop_prompt="Stop",

key="rec"

)


if audio:

 audio_bytes = audio["bytes"]

 with open("voice.wav","wb") as f:

  f.write(audio_bytes)


 transcription = engine.client.audio.transcriptions.create(

  file=open("voice.wav","rb"),

  model="whisper-large-v3"

 )

 spoken_text = transcription.text


 st.success("You said:")

 st.write(spoken_text)


 answer = engine.ask(spoken_text)

 st.success(answer)


 tts=gTTS(answer)

 tts.save("voice_reply.mp3")

 st.audio("voice_reply.mp3")



# ---------------------------
# GAMIFICATION PANEL
# ---------------------------

st.subheader("🏆 Learning Progress")


score=st.slider(

"Quiz Score",

0,

100

)


if st.button("Update Score"):

 engine.update_score(score)

 st.success("Progress Updated!")
