import streamlit as st
import pandas as pd
import numpy as np

def render_data_summary(df: pd.DataFrame):
    """
    Render a comprehensive dashboard for the dataframe.
    """
    st.write("### 📊 Dataset Dashboard")
    
    # 1. VITALS ROW
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", df.shape[0])
    c2.metric("Columns", df.shape[1])
    
    dupes = df.duplicated().sum()
    c3.metric("Duplicates", dupes, delta=f"{dupes/len(df):.1%}" if len(df) > 0 else None, delta_color="inverse")
    
    mem_bytes = df.memory_usage(deep=True).sum()
    mem_mb = mem_bytes / (1024 * 1024)
    c4.metric("Memory", f"{mem_mb:.2f} MB")
    
    # 2. TABS FOR DETAILS
    tab1, tab2, tab3 = st.tabs(["👁️ Data Preview", "📉 Statistics & Health", "ℹ️ Column Info"])
    
    with tab1:
        st.dataframe(df.head(10))
        st.caption(f"Showing first 10 rows of {len(df)}.")

    with tab2:
        # TYPE BREAKDOWN
        types = df.dtypes.value_counts()
        
        # Identify specific types
        num_cols = df.select_dtypes(include=np.number).columns
        cat_cols = df.select_dtypes(include=['object', 'category']).columns
        bool_cols = df.select_dtypes(include='bool').columns
        date_cols = df.select_dtypes(include='datetime').columns
        
        st.write("#### 1. Column Composition")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Numeric", len(num_cols))
        k2.metric("Categorical", len(cat_cols))
        k3.metric("Boolean", len(bool_cols))
        k4.metric("DateTime", len(date_cols))
        
        st.divider()
        
        # MISSING VALUES
        st.write("#### 2. Missing Values")
        missing = df.isnull().sum()
        missing = missing[missing > 0].sort_values(ascending=False)
        
        if missing.empty:
            st.success("✅ No missing values found!")
        else:
            c_miss1, c_miss2 = st.columns([2, 1])
            with c_miss1:
                st.bar_chart(missing)
            with c_miss2:
                st.dataframe(missing.to_frame("Count"))
        
        st.divider()
        
        # NUMERIC STATS
        if not num_cols.empty:
            st.write("#### 3. Numeric Statistics")
            st.dataframe(df[num_cols].describe().T)

    with tab3:
        st.write("#### Column Details")
        
        cols_info = []
        for col in df.columns:
            col_type = df[col].dtype
            n_unique = df[col].nunique()
            n_miss = df[col].isnull().sum()
            
            # Example value
            example = df[col].dropna().iloc[0] if not df[col].dropna().empty else "All NaNs"
            
            cols_info.append({
                "Column": col,
                "Type": str(col_type),
                "Unique": n_unique,
                "Missing": n_miss,
                "Example": str(example)[:50] # Truncate
            })
            
        st.dataframe(pd.DataFrame(cols_info))
