import streamlit as st
from .manual.main import render_manual_evaluation
from .auto.main import render_auto_evaluation

def render_model_evaluation_page():
    st.title("📉 Model Evaluation")
    
    tab1, tab2 = st.tabs(["Manual Mode", "Automatic Mode"])
    
    with tab1:
        render_manual_evaluation()
    
    with tab2:
        render_auto_evaluation()
