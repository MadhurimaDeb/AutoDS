import pandas as pd
import streamlit as st
import os

def infer_and_convert_dtypes(df):
    """
    Intelligently infer and convert object columns to datetime.
    """
    if df is None: return None
    
    # 1. Identify candidate object columns
    object_cols = df.select_dtypes(include=['object']).columns
    
    for col in object_cols:
        try:
            # 2. Attempt coercion
            # We use errors='coerce' to turn bad strings into NaT
            converted = pd.to_datetime(df[col], errors='coerce')
            
            # 3. Check success rate
            # If the column was empty or all NaNs, ignore
            non_na_original = df[col].notna().sum()
            if non_na_original == 0:
                continue
                
            non_na_converted = converted.notna().sum()
            
            # 4. Threshold: If > 80% of Non-NA values successfully converted, accept it
            # This avoids converting columns that are mostly text but happen to have 1 date
            if (non_na_converted / non_na_original) > 0.8:
                df[col] = converted
                
        except Exception:
            continue
            
    return df

def load_data(uploaded_file):
    """Load CSV or Excel file."""
    if uploaded_file is None:
        return None

    df = None
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    elif uploaded_file.name.endswith(".parquet"): # Just in case
        df = pd.read_parquet(uploaded_file)

    if df is not None:
        return infer_and_convert_dtypes(df)
        
    return None


from core.data_manager import DataManager

def save_to_cloud(df, filename):
    """Save dataset to local storage with versioning."""
    
    saved_path = DataManager.save_dataset(df, filename, action_description=f"Imported dataset '{filename}' with shape {df.shape}")
    dataset_name = os.path.basename(saved_path)
    
    # Also keep in session state for immediate access transparency
    if "cloud_datasets" not in st.session_state:
        st.session_state["cloud_datasets"] = {}
    
    st.session_state["cloud_datasets"][dataset_name] = df
    
    return f"Dataset saved as '{dataset_name}'"
