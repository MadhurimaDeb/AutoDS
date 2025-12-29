import streamlit as st
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def render_auto_evaluation():
    st.header("📋 Auto-Evaluation Report")
    
    if "trained_model" not in st.session_state:
        st.warning("No trained model found.")
        return
        
    task_type = st.session_state["model_task"]
    y_test = st.session_state["model_y_test"]
    preds = st.session_state["model_preds"]
    
    st.subheader("Performance Metrics")
    col1, col2, col3 = st.columns(3)
    
    if task_type == "Classification":
        # Handle string labels vs int labels for precision/recall (use macro average safely)
        # For simplicity in this demo, catch exceptions if binary logic fails on multiclass
        try:
            acc = accuracy_score(y_test, preds)
            f1 = f1_score(y_test, preds, average='weighted')
            prec = precision_score(y_test, preds, average='weighted')
            
            col1.metric("Accuracy", f"{acc:.4f}")
            col2.metric("F1 Score", f"{f1:.4f}")
            col3.metric("Precision", f"{prec:.4f}")
            
            st.success("Model performs well!" if acc > 0.8 else "Model might need improvement.")
        except Exception as e:
            st.error(f"Could not calculate some metrics: {e}")
            
    else:
        rmse = mean_squared_error(y_test, preds, squared=False)
        mae = mean_absolute_error(y_test, preds)
        r2 = r2_score(y_test, preds)
        
        col1.metric("RMSE", f"{rmse:.4f}")
        col2.metric("MAE", f"{mae:.4f}")
        col3.metric("R2 Score", f"{r2:.4f}")
        
        st.success("High R2 Score indicates good fit!" if r2 > 0.8 else "Consider trying a different model.")
