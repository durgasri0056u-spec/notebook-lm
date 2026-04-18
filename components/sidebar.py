import streamlit as st
import os
from core.document_processor import process_pdf
from core.vector_store import get_db

UPLOAD_DIR = "storage/uploads"


def render_sidebar():
    st.sidebar.header("📂 Document Manager")

    file = st.sidebar.file_uploader("Upload PDF", type=["pdf"])

    if file:
        path = os.path.join(UPLOAD_DIR, file.name)

        with st.spinner("Processing PDF..."):
            with open(path, "wb") as f:
                f.write(file.read())

            chunks = process_pdf(path)
            db = get_db()
            db.add_documents(chunks)
            db.persist()

        st.sidebar.success("Uploaded & Indexed ✅")

    files = os.listdir(UPLOAD_DIR)
    selected = st.sidebar.multiselect("Select Documents", files)

    st.sidebar.write("Selected:", selected)

    st.session_state["docs"] = selected
    st.session_state["web"] = st.sidebar.checkbox("Enable Web Search")