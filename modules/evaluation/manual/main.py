import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.metrics import confusion_matrix, roc_curve, auc, mean_absolute_error, r2_score
import numpy as np

def render_manual_evaluation():
    st.header("📈 Manual Evaluation")
    
    if "trained_model" not in st.session_state:
        st.warning("No trained model found. Please train a model in the 'Model Preparation' tab first.")
        return
        
    task_type = st.session_state["model_task"]
    y_test = st.session_state["model_y_test"]
    preds = st.session_state["model_preds"]
    
    st.write(f"Evaluating Model for Task: **{task_type}**")
    
    if task_type == "Classification":
        option = st.selectbox("Select Plot", ["Confusion Matrix", "Metrics Summary", "Feature Importance"])
        
        if option == "Confusion Matrix":
            cm = confusion_matrix(y_test, preds)
            fig = px.imshow(cm, text_auto=True, title="Confusion Matrix")
            st.plotly_chart(fig)
            
        elif option == "Metrics Summary":
            from sklearn.metrics import classification_report
            report = classification_report(y_test, preds, output_dict=True)
            df_report = pd.DataFrame(report).transpose()
            st.dataframe(df_report)
            
            with st.expander("🤖 Explain Metrics"):
                if st.button("Analyze Performance"):
                    summary = f"Accuracy: {report['accuracy']}\nMacro Avg F1: {report['macro avg']['f1-score']}"
                    prompt = "Explain these classification metrics. Is the model good?"
                    insight = st.session_state.chat_manager.generate_insight(prompt, summary)
                    st.write(insight)
            
        elif option == "Feature Importance":
            model = st.session_state["trained_model"]
            if hasattr(model, "feature_importances_"):
                # We need column names from X_test, which we saved
                if "model_X_test" in st.session_state:
                    feats = st.session_state["model_X_test"].columns
                    importances = model.feature_importances_
                    df_imp = pd.DataFrame({"Feature": feats, "Importance": importances}).sort_values(by="Importance", ascending=False)
                    fig = px.bar(df_imp, x="Importance", y="Feature", orientation='h', title="Feature Importance")
                    st.plotly_chart(fig)
                else:
                    st.warning("Feature names not found.")
            else:
                st.info("This model type does not support built-in feature importance (e.g., Logistic Regression or Neural Networks). Experimental SHAP support coming soon.")
            
    elif task_type == "Regression":
        option = st.selectbox("Select Plot", ["Actual vs Predicted", "Residuals", "Feature Importance"])
        
        if option == "Actual vs Predicted":
            df_res = pd.DataFrame({"Actual": y_test, "Predicted": preds})
            fig = px.scatter(df_res, x="Actual", y="Predicted", title="Actual vs Predicted")
            fig.add_shape(type="line", line=dict(dash="dash"), x0=y_test.min(), y0=y_test.min(), x1=y_test.max(), y1=y_test.max())
            st.plotly_chart(fig)
            
        elif option == "Residuals":
            residuals = y_test - preds
            fig = px.histogram(residuals, title="Residual Distribution", nbins=30)
            st.plotly_chart(fig)
            
        elif option == "Feature Importance":
            model = st.session_state["trained_model"]
            if hasattr(model, "feature_importances_"):
                if "model_X_test" in st.session_state:
                    feats = st.session_state["model_X_test"].columns
                    importances = model.feature_importances_
                    df_imp = pd.DataFrame({"Feature": feats, "Importance": importances}).sort_values(by="Importance", ascending=False)
                    fig = px.bar(df_imp, x="Importance", y="Feature", orientation='h', title="Feature Importance")
                    st.plotly_chart(fig)
            else:
                st.info("This model type does not support built-in feature importance.")
