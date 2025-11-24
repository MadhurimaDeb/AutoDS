import streamlit as st

# Set page layout
st.set_page_config(page_title="AutoDS", layout="wide")

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "home"


# -----------------------------
#  NAVIGATION FUNCTIONS
# -----------------------------
def go_home():
    st.session_state.page = "home"

def go_exploration():
    st.session_state.page = "exploration"

def go_model():
    st.session_state.page = "model"


# -----------------------------
#  PAGE: HOME (2 BUTTON SCREEN)
# -----------------------------
def render_home():

    st.title("AutoDS — Main Dashboard")
    st.write("Choose an option:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📊 Data Exploration",
                     use_container_width=True,
                     key="exploration_btn"):
            go_exploration()

    with col2:
        if st.button("🤖 Machine Learning Model",
                     use_container_width=True,
                     key="model_btn"):
            go_model()


# -----------------------------
#  PAGE: DATA EXPLORATION
# -----------------------------
def render_exploration():
    st.title("📊 Data Exploration")
    st.write("This is your Data Exploration Page.")

    if st.button("⬅ Back to Home", key="home1"):
        go_home()


# -----------------------------
#  PAGE: ML MODEL
# -----------------------------
def render_ml_model():
    st.title("🤖 Machine Learning Model")
    st.write("This is your ML Model Page.")

    if st.button("⬅ Back to Home", key="home2"):
        go_home()


# -----------------------------
#  RENDER BASED ON PAGE
# -----------------------------
if st.session_state.page == "home":
    render_home()

elif st.session_state.page == "exploration":
    render_exploration()

elif st.session_state.page == "model":
    render_ml_model()
