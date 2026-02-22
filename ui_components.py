import streamlit as st


def glass_card(title):

 st.markdown(

 f"""

 <div style="

 background:rgba(255,255,255,0.05);

 padding:20px;

 border-radius:18px;

 backdrop-filter:blur(15px);

 margin-bottom:20px;

 ">

 <h3>{title}</h3>

 </div>

 """,

 unsafe_allow_html=True

 )
