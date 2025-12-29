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

init_state()

# ---------------------------
# SIDEBAR NAVIGATION
# ---------------------------
with st.sidebar:
    st.title("📂 AutoDS Navigation")

    if st.button("Import & Save Data on Cloud"): st.session_state.page = "import"
    if st.button("Data Cleaning"): st.session_state.page = "cleaning"
    if st.button("EDA"): st.session_state.page = "eda"
    if st.button("Feature Engineering"): st.session_state.page = "fe"
    if st.button("Model Preparation"): st.session_state.page = "model"
    if st.button("Model Evaluation"): st.session_state.page = "evaluation"

    st.write("---")
    if st.button("💬 Chat with AI"):
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
    elif page == "import": placeholder_page("Import & Save Data on Cloud")
    elif page == "cleaning": placeholder_page("Data Cleaning")
    elif page == "eda": placeholder_page("Exploratory Data Analysis (EDA)")
    elif page == "fe": placeholder_page("Feature Engineering")
    elif page == "model": placeholder_page("Model Preparation")
    elif page == "evaluation": placeholder_page("Model Evaluation")

# ---------------------------
# GEMINI AI SETUP (v2.5)
# ---------------------------
API_KEY = os.getenv("GOOGLE_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("models/gemini-2.5-flash")  # ⭐ BEST FOR YOU
else:
    model = None

SYSTEM_PROMPT = """
You are AutoDS AI Assistant.
You must:
- Answer all questions related to ML, DL, Python, SQL, Statistics, Analytics, Data Science.
- Guide the user through this AutoDS application (which button to click next).
- Understand user intent from behavior.
- If a dataset is uploaded, analyze it deeply (summary, insights, EDA guidance).
- Be friendly, helpful, and precise.
"""

# ---------------------------
# CHAT PANEL
# ---------------------------
if st.session_state.chat_open and chat_col:
    with chat_col:
        st.title("🤖 Assistant")
        if st.button("Close Panel"): st.session_state.chat_open = False

        st.write("### Ask something:")
        user_message = st.text_input("Type your message", key="chat_box")

        st.write("### Chat:")
        if user_message:
            st.write(f"**You:** {user_message}")

            if model:
                try:
                    response = model.generate_content(SYSTEM_PROMPT + "\nUser: " + user_message)
                    st.success(response.text)
                except Exception as e:
                    st.error(f"AI Error: {str(e)}")
            else:
                st.warning("Gemini API key missing or model failed to load.")
