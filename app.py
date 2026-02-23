import streamlit as st
from rag_engine import MindGapEngine
from database import load_profile, add_score
from analytics import show_analytics
from voice_utils import text_to_voice

from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
import os

st.set_page_config(
    layout="wide",
    page_title="MindGap AI"
)

# ---------- CSS ----------
css_path="assets/styles.css"

if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


engine = MindGapEngine()
profile = load_profile()

# Sidebar

st.sidebar.title("MindGap AI")

st.sidebar.metric(
    "XP",
    profile["xp"]
)

st.sidebar.write(profile["achievements"])


# ---------- Upload ----------

file = st.file_uploader(
    "Upload Study Material",
    ["pdf","png","jpg","txt"]
)


def extract(file):

    if file.type=="application/pdf":

        pdf = PdfReader(file)

        text=""

        for p in pdf.pages:
            text+=p.extract_text() or ""

        return text


    if "image" in file.type:

        img=Image.open(file)

        return pytesseract.image_to_string(img)

    return file.read().decode()


if file:

    txt = extract(file)

    st.success(
        engine.process_document(txt)
    )


# ---------- ASK ----------

question = st.text_area(
    "Ask Tutor"
)

if st.button("Ask"):

    ans = engine.ask(question)

    st.success(ans)

    audio = text_to_voice(ans)

    if audio:
        st.audio(audio)


# ---------- QUIZ ----------

if st.button("Generate Quiz"):

    st.info(
        engine.generate_quiz(question)
    )


score = st.slider(
    "Quiz Score",
    0,
    100
)

if st.button("Update Score"):

    add_score(score)

    st.success("Saved")


show_analytics()
