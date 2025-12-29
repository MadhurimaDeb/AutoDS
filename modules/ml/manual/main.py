import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import accuracy_score, mean_squared_error
import pickle

def render_manual_ml():
    st.header("🧠 Manual Model Building")
    
    if "active_dataset" not in st.session_state:
        st.warning("Please import a dataset first.")
        return

    dataset_name = st.session_state["active_dataset"]
    df = st.session_state["cloud_datasets"][dataset_name]
    
    col1, col2 = st.columns(2)
    
    with col1:
        target = st.selectbox("Select Target Variable", df.columns)
    
    with col2:
        task_type = st.selectbox("Task Type", ["Classification", "Regression"])
        
    features = st.multiselect("Select Features (Leave empty for all except target)", [c for c in df.columns if c != target])
    
    if not features:
        features = [c for c in df.columns if c != target]
        
    with st.expander("🤖 AI Method Recommendation"):
        if st.button("Suggest Model"):
            summary = f"Target: {target} (Type: {df[target].dtype})\nFeatures: {len(features)}\nRows: {len(df)}"
            prompt = "Suggest the best machine learning algorithm for this dataset and target variable."
            insight = st.session_state.chat_manager.generate_insight(prompt, summary)
            st.write(insight)
        
    model_choice = st.selectbox("Select Algorithm", ["Random Forest", "Linear/Logistic Regression"])
    
    params = {}
    if model_choice == "Random Forest":
        n_estimators = st.slider("n_estimators", 10, 500, 100)
        max_depth = st.slider("max_depth", 1, 50, 10)
        params = {"n_estimators": n_estimators, "max_depth": max_depth}
        
    if st.button("Train Model"):
        X = df[features]
        y = df[target]
        
        # Handle non-numeric features basic
        X = pd.get_dummies(X, drop_first=True)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        if task_type == "Classification":
            if model_choice == "Random Forest":
                model = RandomForestClassifier(**params)
            else:
                model = LogisticRegression()
            metric_name = "Accuracy"
        else:
            if model_choice == "Random Forest":
                model = RandomForestRegressor(**params)
            else:
                model = LinearRegression()
            metric_name = "RMSE"
            
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        
        if task_type == "Classification":
            score = accuracy_score(y_test, preds)
            st.success(f"Model Trained! Accuracy: {score:.4f}")
        else:
            score = mean_squared_error(y_test, preds, squared=False)
            st.success(f"Model Trained! RMSE: {score:.4f}")
            
        # Save to session for Evaluation module
        st.session_state["trained_model"] = model
        st.session_state["model_X_test"] = X_test
        st.session_state["model_y_test"] = y_test
        st.session_state["model_preds"] = preds
        st.session_state["model_task"] = task_type
        st.session_state["model_target"] = target
