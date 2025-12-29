import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from core.data_manager import DataManager

def render_auto_feature_engineering():
    st.header("🤖 Auto-Feature Engineering")
    
    if "active_dataset" not in st.session_state:
        st.warning("Please import a dataset first.")
        return

    dataset_name = st.session_state["active_dataset"]
    df = st.session_state["cloud_datasets"][dataset_name]
    
    st.info("Pipeline Strategy:\n1. Encode all categorical variables (Label Encoding for high cardinality, One-Hot for low)\n2. Scale all numeric variables (StandardScaler)")
    
    if st.button("🚀 Run Auto-Features"):
        df_new = df.copy()
        report = []
        
        # 1. Handle Categorical
        cat_cols = df_new.select_dtypes(include=['object', 'category']).columns
        for col in cat_cols:
            if df_new[col].nunique() < 10:
                df_new = pd.get_dummies(df_new, columns=[col], drop_first=True)
                report.append(f"One-Hot Encoded: {col}")
            else:
                le = LabelEncoder()
                df_new[col] = le.fit_transform(df_new[col].astype(str))
                report.append(f"Label Encoded: {col}")
                
        # 2. Handle Numeric (Scaling)
        num_cols = df_new.select_dtypes(include=['number']).columns
        # Exclude target variable if known? For now scale everything except potential ID-like columns (heuristic needed)
        # Simple heuristic: don't scale int columns that act as IDs? 
        # For simplicity, scale floats.
        float_cols = df_new.select_dtypes(include=['float']).columns
        if not float_cols.empty:
            scaler = StandardScaler()
            df_new[float_cols] = scaler.fit_transform(df_new[float_cols])
            report.append(f"Standard Scaled {len(float_cols)} columns.")
            
        DataManager.save_dataset(df_new, dataset_name, version_note="auto_fe")
        st.session_state["cloud_datasets"][dataset_name] = df_new
        
        st.success("Feature Engineering Complete!")
        for r in report:
            st.write(f"- {r}")
        st.dataframe(df_new.head())
