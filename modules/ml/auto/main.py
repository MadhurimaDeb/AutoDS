import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import accuracy_score, mean_squared_error

def render_auto_ml():
    st.header("⚡ Auto-ML")
    
    if "active_dataset" not in st.session_state:
        st.warning("Please import a dataset first.")
        return

    dataset_name = st.session_state["active_dataset"]
    df = st.session_state["cloud_datasets"][dataset_name]
    
    col1, col2 = st.columns(2)
    with col1:
        target = st.selectbox("Select Target Variable (Auto-ML)", df.columns)
    with col2:
        task_type = st.selectbox("Task Type (Auto-ML)", ["Classification", "Regression"])

    if st.button("🚀 Run Auto-ML"):
        st.write("Training multiple models...")
        X = df.drop(columns=[target])
        y = df[target]
        X = pd.get_dummies(X, drop_first=True)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        results = {}
        models = {}
        
        if task_type == "Classification":
            algos = {
                "RandomForest": RandomForestClassifier(),
                "GradientBoosting": GradientBoostingClassifier()
            }
            metric = accuracy_score
        else:
            algos = {
                "RandomForest": RandomForestRegressor(),
                "GradientBoosting": GradientBoostingRegressor()
            }
            metric = lambda y, p: mean_squared_error(y, p, squared=False)
            
        for name, algo in algos.items():
            algo.fit(X_train, y_train)
            preds = algo.predict(X_test)
            score = metric(y_test, preds)
            results[name] = score
            models[name] = algo
            st.write(f"Tested {name}: Score = {score:.4f}")
            
        # Pick best
        if task_type == "Classification":
            best_name = max(results, key=results.get)
        else:
            best_name = min(results, key=results.get) # Lower RMSE is better
            
        st.success(f"Best Model: {best_name} with Score: {results[best_name]:.4f}")
        
        # Save best
        st.session_state["trained_model"] = models[best_name]
        st.session_state["model_X_test"] = X_test
        st.session_state["model_y_test"] = y_test
        st.session_state["model_preds"] = models[best_name].predict(X_test)
        st.session_state["model_task"] = task_type
