import streamlit as st
import pickle
import io

def render_export_page():
    st.title("💾 Model Export")
    
    if "trained_model" not in st.session_state:
        st.warning("No trained model found. Please train a model first.")
        return
        
    model = st.session_state["trained_model"]
    task_type = st.session_state.get("model_task", "Unknown")
    
    st.write(f"### Ready to Export: {type(model).__name__}")
    st.write(f"**Task Type:** {task_type}")
    
    # Serialization
    buffer = io.BytesIO()
    pickle.dump(model, buffer)
    buffer.seek(0)
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="Download Model (.pkl)",
            data=buffer,
            file_name=f"autods_model_{task_type.lower()}.pkl",
            mime="application/octet-stream"
        )
        
    with col2:
        st.info("Onnx export coming soon!")
