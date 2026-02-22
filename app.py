import streamlit as st
from rag_engine import MindGapEngine
from database import load_profile,add_score
from analytics import show_analytics
from voice_utils import text_to_voice

from streamlit_mic_recorder import mic_recorder

from PyPDF2 import PdfReader

from PIL import Image

import pytesseract


st.set_page_config(

 layout="wide",

 page_title="MindGap AI"

)


# load css

with open("assets/styles.css") as f:

 st.markdown(

 f"<style>{f.read()}</style>",

 unsafe_allow_html=True

 )


engine=MindGapEngine()

profile=load_profile()


# sidebar

st.sidebar.title("MindGap AI")

st.sidebar.metric(

"XP",

profile["xp"]

)

st.sidebar.write(profile["achievements"])



# upload

file=st.file_uploader(

"Upload Study Material",

["pdf","png","jpg","txt"]

)


def extract(file):

 if file.type=="application/pdf":

  pdf=PdfReader(file)

  txt=""

  for p in pdf.pages:

   txt+=p.extract_text()

  return txt

 if "image" in file.type:

  img=Image.open(file)

  return pytesseract.image_to_string(img)

 return file.read().decode()



if file:

 txt=extract(file)

 st.success(

 engine.process_document(txt)

 )


question=st.text_area(

"Ask Tutor"

)


if st.button("Ask"):

 ans=engine.ask(question)

 st.success(ans)

 audio=text_to_voice(ans)

 st.audio(audio)



# voice

audio=mic_recorder()

if audio:

 open("voice.wav","wb").write(

 audio["bytes"]

 )


 t=engine.client.audio.transcriptions.create(

 file=open("voice.wav","rb"),

 model="whisper-large-v3"

 )

 ans=engine.ask(t.text)

 st.success(ans)

 st.audio(text_to_voice(ans))



# quiz

if st.button("Generate Quiz"):

 st.info(

 engine.generate_quiz(question)

 )


score=st.slider(

"Quiz Score",

0,

100

)

if st.button("Update Score"):

 add_score(score)

 st.success("Saved")



show_analytics()
