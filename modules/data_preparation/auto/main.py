import streamlit as st
import pandas as pd
from core.data_manager import DataManager

def render_auto_cleaning():
    st.header("🤖 Auto-Cleaning")
    
    if "active_dataset" not in st.session_state:
        st.warning("Please import a dataset first.")
        return

    dataset_name = st.session_state["active_dataset"]
    df = st.session_state["cloud_datasets"][dataset_name]
    
    st.write("This module automatically detects and fixes common data quality issues.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("**What it does:**\n- Drops columns with > 50% missing values\n- Fills numeric missing values with Median\n- Fills categorical missing values with Mode\n- Drops duplicate rows")
    
    if st.button("✨ Run Auto-Clean Pipeline"):
        df_new = df.copy()
        
        report = []
        
        # 1. Drop high missing
        limit = len(df_new) * 0.5
        dropped_cols = [c for c in df_new.columns if df_new[c].isnull().sum() > limit]
        df_new = df_new.drop(columns=dropped_cols)
        if dropped_cols:
            report.append(f"Dropped {len(dropped_cols)} columns with > 50% missing: {dropped_cols}")
            
        # 2. Duplicates
        dupes = df_new.duplicated().sum()
        if dupes > 0:
            df_new = df_new.drop_duplicates()
            report.append(f"Dropped {dupes} duplicate rows.")
            
        # 3. Fill Missing
        num_cols = df_new.select_dtypes(include=['number']).columns
        cat_cols = df_new.select_dtypes(exclude=['number']).columns
        
        for c in num_cols:
            if df_new[c].isnull().sum() > 0:
                df_new[c] = df_new[c].fillna(df_new[c].median())
                
        for c in cat_cols:
            if df_new[c].isnull().sum() > 0:
                df_new[c] = df_new[c].fillna(df_new[c].mode()[0])
                
        report.append("Filled missing values (Numeric -> Median, Categorical -> Mode).")
        
        # Save
        DataManager.save_dataset(df_new, dataset_name, version_note="auto_clean")
        st.session_state["cloud_datasets"][dataset_name] = df_new
        
        st.success("Auto-Cleaning Complete!")
        for item in report:
            st.write(f"- {item}")
            
        st.dataframe(df_new.head())
