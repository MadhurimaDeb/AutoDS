import streamlit as st
from .manual.main import render_manual_ml
from .auto.main import render_auto_ml

def render_model_building_page():
    st.title("🤖 Model Building")
    
    tab1, tab2 = st.tabs(["Manual Mode", "Automatic Mode"])
    
    with tab1:
        render_manual_ml()
    
    with tab2:
        render_auto_ml()
