import streamlit as st
from .manual.main import render_manual_cleaning
from .auto.main import render_auto_cleaning

def render_data_preparation_page():
    st.title("🧹 Data Preparation")
    
    tab1, tab2 = st.tabs(["Manual Mode", "Automatic Mode"])
    
    with tab1:
        render_manual_cleaning()
    
    with tab2:
        render_auto_cleaning()
