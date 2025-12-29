import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from core.data_manager import DataManager

def render_manual_feature_engineering():
    st.header("🛠️ Manual Feature Engineering")
    
    if "active_dataset" not in st.session_state:
        st.warning("Please import a dataset first.")
        return

    dataset_name = st.session_state["active_dataset"]
    df = st.session_state["cloud_datasets"][dataset_name]
    
    st.write(f"Refining: **{dataset_name}**")
    st.dataframe(df.head())
    
    with st.expander("🤖 Ask AI for Feature Ideas"):
        if st.button("Suggest Features"):
            summary = f"Columns: {list(df.columns)}"
            prompt = "Suggest 3 new features I could engineer from these columns."
            insight = st.session_state.chat_manager.generate_insight(prompt, summary)
            st.write(insight)
    
    col1, col2 = st.columns(2)
    
    # --- ENCODING ---
    with col1:
        st.subheader("Categorical Encoding")
        cat_cols = df.select_dtypes(include=['object', 'category']).columns
        
        target_col = st.selectbox("Select Column to Encode", cat_cols)
        method = st.selectbox("Method", ["Label Encoding", "One-Hot Encoding"])
        
        if st.button("Apply Encoding"):
            df_new = df.copy()
            if method == "Label Encoding":
                le = LabelEncoder()
                df_new[target_col] = le.fit_transform(df_new[target_col].astype(str))
                note = "label_encoded"
            elif method == "One-Hot Encoding":
                df_new = pd.get_dummies(df_new, columns=[target_col], prefix=target_col)
                note = "one_hot"
                
            DataManager.save_dataset(df_new, dataset_name, version_note=note)
            st.session_state["cloud_datasets"][dataset_name] = df_new
            st.success(f"Applied {method} on {target_col}")
            st.rerun()

    # --- SCALING ---
    with col2:
        st.subheader("Numerical Scaling")
        num_cols = df.select_dtypes(include=['number']).columns
        
        target_cols_scale = st.multiselect("Select Columns to Scale", num_cols)
        scale_method = st.selectbox("Scaling Method", ["StandardScaler (Z-Score)", "MinMaxScaler (0-1)"])
        
        if st.button("Apply Scaling"):
            if target_cols_scale:
                df_new = df.copy()
                if scale_method.startswith("Standard"):
                    scaler = StandardScaler()
                else:
                    scaler = MinMaxScaler()
                    
                df_new[target_cols_scale] = scaler.fit_transform(df_new[target_cols_scale])
                
                DataManager.save_dataset(df_new, dataset_name, version_note="scaled")
                st.session_state["cloud_datasets"][dataset_name] = df_new
                st.success(f"Scaled {len(target_cols_scale)} columns.")
                st.rerun()
