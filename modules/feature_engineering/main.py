import streamlit as st
from .manual.main import render_manual_feature_engineering
from .auto.main import render_auto_feature_engineering

def render_feature_engineering_page():
    st.title("🔧 Feature Engineering")
    
    tab1, tab2 = st.tabs(["Manual Mode", "Automatic Mode"])
    
    with tab1:
        render_manual_feature_engineering()
    
    with tab2:
        render_auto_feature_engineering()
