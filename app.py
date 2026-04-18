import streamlit as st
from components.sidebar import render_sidebar
from components.chat import render_chat
from components.notes import render_notes

st.set_page_config(layout="wide")

col1, col2, col3 = st.columns([1,2,1])

with col1:
    render_sidebar()
with col2:
    render_chat()
with col3:
    render_notes()