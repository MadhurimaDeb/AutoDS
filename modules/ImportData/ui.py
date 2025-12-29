import streamlit as st

def render_upload_ui():
    st.subheader("📤 Upload Dataset")
    return st.file_uploader(
        "Choose a CSV or Excel file",
        type=["csv", "xlsx"],
        key="import_uploader"
    )

def render_save_button():
    st.subheader("💾 Save Dataset to Cloud Memory")
    return st.button("Save to Cloud")

def render_next_step_button():
    st.subheader("➡ Next Step")
    return st.button("Proceed to Data Cleaning")
