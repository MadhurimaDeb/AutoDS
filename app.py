import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env
load_dotenv()

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(page_title="AutoDS", page_icon="🧠", layout="wide")

# ---------------------------
# SESSION STATE
# ---------------------------
def init_state():
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "chat_open" not in st.session_state:
        st.session_state.chat_open = False

    if "action_log" not in st.session_state:
        st.session_state["action_log"] = []
    if "nav_history" not in st.session_state:
        st.session_state["nav_history"] = []

init_state()

def go_to_page(page_name):
    """Navigate to a page and push current to history."""
    if st.session_state.page != page_name:
        st.session_state.nav_history.append(st.session_state.page)
        st.session_state.page = page_name
        st.rerun()

def go_back():
    """Pop previous page from history."""
    if st.session_state.nav_history:
        prev_page = st.session_state.nav_history.pop()
        st.session_state.page = prev_page
        st.rerun()

def go_home():
    """Clear history and go home."""
    st.session_state.nav_history = []
    st.session_state.page = "home"
    st.rerun()

# ---------------------------
# SIDEBAR NAVIGATION
# ---------------------------
with st.sidebar:
    st.title("📂 AutoDS Navigation")

    if st.button("Import & Save Data on Cloud", use_container_width=True): go_to_page("import")
    if st.button("Data Cleaning", use_container_width=True): go_to_page("cleaning")
    if st.button("EDA", use_container_width=True): go_to_page("eda")
    if st.button("Feature Engineering", use_container_width=True): go_to_page("fe")
    if st.button("Model Preparation", use_container_width=True): go_to_page("model")
    if st.button("Model Evaluation", use_container_width=True): go_to_page("evaluation")
    if st.button("Export Model", use_container_width=True): go_to_page("export")

    st.write("---")
    if st.button("💬 Chat with AI", use_container_width=True):
        st.session_state.chat_open = not st.session_state.chat_open

# ---------------------------
# LAYOUT SPLIT
# ---------------------------
if st.session_state.chat_open:
    main_col, chat_col = st.columns([3, 1.2])
else:
    main_col, = st.columns([1])
    chat_col = None

# ---------------------------
# PAGES
# ---------------------------
def render_home():
    st.title("AutoDS – No-Code Machine Learning Suite")
    
    # Dynamic Dashboard
    col1, col2, col3 = st.columns(3)
    
    dataset = st.session_state.get("active_dataset", "None")
    col1.metric("Active Dataset", dataset)
    
    model = st.session_state.get("trained_model", None)
    model_name = type(model).__name__ if model else "None"
    col2.metric("Trained Model", model_name)
    
    col3.metric("Mode", "Dual-Mode (Auto/Manual)")
    
    st.divider()
    
    st.header("About the App")
    st.write("""
        AutoDS is an end-to-end no-code data science and machine learning platform that allows you to:
        - Upload and store datasets securely
        - Perform automated or manual data cleaning
        - Run exploratory data analysis (EDA)
        - Engineer features
        - Train and tune ML models
        - Evaluate performance with multiple metrics
    """)
    st.header("Developer")
    st.write("**Madhurima Deb**")
    st.header("Contact Information")
    st.write("📧 Email: mayurakshideb32@gmail.com")
    st.write("🔗 LinkedIn: https://www.linkedin.com/in/madhurima-deb/")
    st.info("Use the left navigation bar to explore each module.")

def placeholder_page(title):
    st.title(title)
    st.write("This page will contain its full functionality later.")

# ---------------------------
# ROUTING
# ---------------------------
with main_col:
    page = st.session_state.page
    
    if page == "home": render_home()
    elif page == "import":
        from modules.ImportData.main import render_data_import_page
        render_data_import_page()
    elif page == "cleaning":
        from modules.data_preparation.main import render_data_preparation_page
        render_data_preparation_page()
    elif page == "eda":
        from modules.eda.main import render_eda_page
        render_eda_page()
    elif page == "fe":
        from modules.feature_engineering.main import render_feature_engineering_page
        render_feature_engineering_page()
    elif page == "model":
        from modules.ml.main import render_model_building_page
        render_model_building_page()
    elif page == "evaluation":
        from modules.evaluation.main import render_model_evaluation_page
        render_model_evaluation_page()
    elif page == "export":
        from modules.export.main import render_export_page
        render_export_page()
    
    # NAVIGATION FOOTER (Back & Home) - Bottom Left
    if page != "home":
        st.divider()
        nav_c1, nav_c2, _ = st.columns([1, 1, 6])
        with nav_c1:
            if st.button("⬅️ Back", use_container_width=True):
                go_back()
        with nav_c2:
            if st.button("🏠 Main Page", use_container_width=True):
                go_home()

# ---------------------------
# GLOBAL DATASET MANAGER
# ---------------------------
from modules.utils import render_dataset_manager
render_dataset_manager()

# ---------------------------
# GEMINI AI SETUP (v2.5)
# ---------------------------
from modules.chat import ChatManager

if "chat_manager" not in st.session_state:
    st.session_state.chat_manager = ChatManager()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------
# CHAT PANEL
# ---------------------------
if st.session_state.chat_open and chat_col:
    with chat_col:
        st.write("### 🤖 AutoDS Assistant")
        if st.button("Close Panel"): 
            st.session_state.chat_open = False
            st.rerun()
            
        # Display Chat History
        chat_container = st.container()
        with chat_container:
            for role, text in st.session_state.chat_history:
                with st.chat_message(role):
                    st.write(text)

        # Input Area
        if prompt := st.chat_input("Ask about your data..."):
            # User Message
            st.session_state.chat_history.append(("user", prompt))
            with chat_container:
                with st.chat_message("user"):
                    st.write(prompt)

            # AI Response
            with chat_container:
                with st.chat_message("assistant"):
                    response_placeholder = st.empty()
                    response_placeholder.write("Thinking...")
                    
                    # Convert history format for Gemini if needed, functionality handled in manager
                    # passing empty history here because manager constructs prompts with current context
                    # If we wanted multi-turn memory with context freshness, we'd handle it carefully.
                    # For now, simplistic "Context + Prompt" is robust for changing data.
                    
                    response_text = st.session_state.chat_manager.generate_response(prompt, []) 
                    response_placeholder.write(response_text)
            
            st.session_state.chat_history.append(("assistant", response_text))
