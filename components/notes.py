import streamlit as st
import os

DIR = "storage/notes"


def render_notes():
    st.subheader("📝 Notes")

    if st.button("Save Note"):
        if "chat" in st.session_state:
            text = st.session_state.chat[-1]["text"]
            name = f"note_{len(os.listdir(DIR))}.md"

            with open(os.path.join(DIR, name), "w") as f:
                f.write(text)

            st.success("Saved ✅")

    if st.button("Download All Notes"):
        all_text = ""
        for f_name in os.listdir(DIR):
            with open(os.path.join(DIR, f_name)) as f:
                all_text += f"\n\n# {f_name}\n" + f.read()

        st.download_button("Download", all_text, file_name="notes.md")

    for f_name in os.listdir(DIR):
        with open(os.path.join(DIR, f_name)) as f:
            st.expander(f_name).write(f.read())