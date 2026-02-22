import streamlit as st
from database import load_profile


def show_analytics():

 profile=load_profile()

 st.subheader("📊 Student Analytics")

 scores=profile["quiz_scores"]

 if scores:

  st.line_chart(scores)

 st.metric(

 "XP",

 profile["xp"]

 )
