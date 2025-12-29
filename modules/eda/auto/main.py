import streamlit as st
import pandas as pd
import plotly.express as px

def render_auto_eda():
    st.header("🤖 Auto-EDA Report")
    
    if "active_dataset" not in st.session_state:
        st.warning("Please import a dataset first.")
        return

    df = st.session_state["cloud_datasets"][st.session_state["active_dataset"]]
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if st.button("Generate Smart Report"):
        st.write("### 1. Dataset Overview")
        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Duplicates", df.duplicated().sum())
        
        st.write("### 2. Column Types")
        st.write(df.dtypes.value_counts())
        
        st.write("### 3. Missing Values Pattern")
        missing_df = df.isnull().sum().reset_index()
        missing_df.columns = ["Column", "Missing Count"]
        missing_df = missing_df[missing_df["Missing Count"] > 0]
        if not missing_df.empty:
            fig_miss = px.bar(missing_df, x="Column", y="Missing Count", title="Missing Values per Column")
            st.plotly_chart(fig_miss)
        else:
            st.success("No missing values detected.")
            
        st.write("### 4. Distributions (Numeric)")
        for col in num_cols:
            try:
                fig = px.histogram(df, x=col, title=f"Distribution of {col}", marginal="box")
                st.plotly_chart(fig, use_container_width=True)
            except: pass
            
        st.write("### 5. Correlation Matrix")
        try:
            numeric_df = df.select_dtypes(include=['number'])
            if not numeric_df.empty:
                corr = numeric_df.corr()
                fig_corr = px.imshow(corr, title="Correlation Matrix", color_continuous_scale='RdBu_r')
                st.plotly_chart(fig_corr, use_container_width=True)
        except: pass
