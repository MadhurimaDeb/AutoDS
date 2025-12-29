import streamlit as st
from .manual.main import render_manual_eda
from .auto.main import render_auto_eda

def render_eda_page():
    st.title("📊 Exploratory Data Analysis")
    
    tab1, tab2 = st.tabs(["Manual Mode", "Automatic Mode"])
    
    with tab1:
        render_manual_eda()
    
    with tab2:
        render_auto_eda()
